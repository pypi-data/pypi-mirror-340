import asyncio
import inspect
from abc import ABC, abstractmethod
from collections.abc import Coroutine
from contextvars import Context
from enum import IntEnum, auto
from typing import Any, Callable, Optional, Self

from .events import Event, on_shutdown
from .group import TaskGroup

__all__ = ["ServiceState", "AbstractService", "service"]


class ServiceState(IntEnum):
    STARTING = auto()
    RUNNING = auto()
    STOPING = auto()
    STOPED = auto()


class AbstractService(ABC):
    """
    Abstract base class for creating asynchronous services.

    Provides a lifecycle management framework (start, stop, restart, wait)
    and task management capabilities for background operations.
    """

    __main__: Optional[asyncio.Task]
    """Main service process task."""
    __name__: str
    """Service name."""
    __waiter__: asyncio.Event
    """Event used to signal service stop completion."""
    __state__: ServiceState
    """Current state of the service."""
    __tasks__: TaskGroup
    """Task group for managing background tasks within the service."""

    on_state_change: Event[ServiceState]
    """Event triggered when the service state changes."""
    on_error: Event[BaseException]
    """Event triggered when an unhandled exception occurs in a background task."""

    def __set_state__(self, state: ServiceState):
        """Internal method to update the service state and emit the change event."""
        self.__state__ = state
        return self.on_state_change.emit(state)

    @property
    def is_stoped(self) -> bool:
        """
        Check if the service is currently stopped.

        Returns:
            bool: True if the service state is STOPED, False otherwise.
        """
        return self.__state__ == ServiceState.STOPED

    @property
    def is_running(self) -> bool:
        """
        Check if the service is currently running.

        Returns:
            bool: True if the service state is RUNNING, False otherwise.
        """
        return self.__state__ == ServiceState.RUNNING

    @property
    def name(self) -> str | None:
        """
        Get the name of the service.

        Returns:
            str | None: The assigned name of the service, or the class name if not provided.
        """
        return self.__name__

    def __init__(self, *, name: Optional[str] = None) -> None:
        """
        Initialize a new service instance.

        Args:
            name (Optional[str]): An optional name for the service. If None,
                                  the class name is used.
        """
        super().__init__()

        self.__name__ = name or self.__class__.__name__
        self.__main__ = None
        self.__state__ = ServiceState.STOPED
        self.__waiter__ = asyncio.Event()
        self.__tasks__ = TaskGroup(error_tolerance=True)
        self.on_error = self.__tasks__.on_error
        self.on_state_change = Event()

    def __on_shutdown__(self, *args, **kwargs):
        """Internal handler called on application shutdown to stop the service."""
        return self.stop()

    def create_task(
        self,
        coro: Coroutine[Any, Any, Any],
        *,
        name: str | None = None,
        context: Context | None = None,
        canceliable: bool = True,
    ) -> asyncio.Task:
        """
        Create and manage a background task within the service's TaskGroup.

        Args:
            coro (Coroutine[Any, Any, Any]): The coroutine to run as a task.
            name (str | None): An optional name for the task.
            context (Context | None): An optional context for the task.
            canceliable (bool): If True (default), the task can be cancelled
                                when the service stops.

        Returns:
            asyncio.Task: The created asyncio Task object.
        """
        return self.__tasks__.create_task(
            coro, name=name, context=context, canceliable=canceliable
        )

    async def start(self) -> None:
        """
        Start the service.

        Transitions the service state through STARTING to RUNNING.
        Executes the `__on_start__` hook, subscribes to the global shutdown event,
        and starts the main `__work__` loop in a background task.
        Does nothing if the service is not currently STOPED.
        """
        if self.is_stoped:
            self.__tasks__.reset_errors()
            self.__waiter__.clear()
            await self.__set_state__(ServiceState.STARTING)
            # Do start
            start_hook = self.__on_start__()
            if inspect.isawaitable(start_hook):
                await start_hook

            # Subscribe to shutdown event
            on_shutdown().add_listener(self.__on_shutdown__)

            # Emit service start event
            await self.__set_state__(ServiceState.RUNNING)

            async def __work_wrapper__(self: Self):
                """Internal wrapper to run __work__ and handle errors."""
                while self.__state__ == ServiceState.RUNNING:
                    try:
                        await self.__work__()
                    except asyncio.CancelledError:
                        # Expected cancellation when stopping
                        break
                    except Exception as err:
                        # Emit other errors
                        await self.on_error.emit(err)
                    # Add a small sleep to prevent tight loop on repeated errors
                    # and yield control.
                    await asyncio.sleep(0.01)

            # Run main process
            self.__main__ = asyncio.create_task(
                __work_wrapper__(self), name=f"{self.__name__}-main"
            )

    async def wait(self) -> None:
        """
        Wait until the service has fully stopped.

        Blocks until the service transitions to the STOPED state.
        If the service is not running, returns immediately.
        """
        if self.is_running or self.__state__ == ServiceState.STOPING:
            await self.__waiter__.wait()

    async def stop(self) -> None:
        """
        Stop the service gracefully.

        Transitions the service state to STOPING.
        Executes the `__on_stop__` hook, unsubscribes from the global shutdown event,
        cancels the main `__work__` task and all background tasks managed by the service,
        and waits for them to complete. Finally, transitions the state to STOPED
        and signals any waiters.
        Does nothing if the service is not currently RUNNING.
        """
        if self.is_running:
            await self.__set_state__(ServiceState.STOPING)

            # Unsubscribe from shutdown event
            _on_shutdown = on_shutdown()
            _on_shutdown.remove_listener(self.__on_shutdown__)

            # Cancel main task first
            if self.__main__ is not None and not self.__main__.done():
                self.__main__.cancel()
                try:
                    # Give the main task a chance to handle cancellation
                    await asyncio.wait_for(self.__main__, timeout=None)
                except asyncio.CancelledError:
                    pass  # Expected cancellation
                except Exception as err:
                    # Log or handle error during main task cancellation/cleanup
                    await self.on_error.emit(err)
            self.__main__ = None

            # Execute stop hook
            stop_hook = self.__on_stop__()
            if inspect.isawaitable(stop_hook):
                try:
                    await stop_hook
                except Exception as err:
                    # Log or handle error during stop hook
                    await self.on_error.emit(err)

            # Cancel and wait for background tasks
            self.__tasks__.cancel()
            await (
                self.__tasks__.wait()
            )  # TaskGroup handles errors internally and emits via on_error

            # Mark as stopped
            await self.__set_state__(ServiceState.STOPED)
            self.__waiter__.set()  # Signal waiters

    async def restart(self) -> None:
        """
        Restart the service.

        Convenience method that calls `stop()` followed by `start()`.
        """
        await self.stop()
        await self.start()

    def __on_start__(self) -> Coroutine[Any, Any, None] | None:
        """
        Optional hook executed during the service startup phase.

        This method can be overridden by subclasses to perform specific
        initialization logic before the main `__work__` loop starts.
        It can be a regular method or an async method.

        Returns:
            Coroutine[Any, Any, None] | None: An awaitable if async logic is needed,
                                               otherwise None.
        """
        return None

    @abstractmethod
    def __work__(self) -> Coroutine[Any, Any, None]:
        """
        Main service logic execution loop.

        This abstract method must be implemented by subclasses. It contains
        the core repetitive work the service performs. It will be called
        repeatedly in a loop while the service is in the RUNNING state.
        If this method raises an exception, it will be caught, emitted via
        `on_error`, and the loop will continue (after a small delay).
        If the service needs to stop based on internal logic, it should
        call `await self.stop()` or simply return/exit the loop structure
        if appropriate (though `stop` is preferred for clean shutdown).

        Returns:
            Coroutine[Any, Any, None]: An awaitable representing one cycle of work.
        """
        pass

    def __on_stop__(self) -> Coroutine[Any, Any, None] | None:
        """
        Optional hook executed during the service stopping phase.

        This method can be overridden by subclasses to perform specific
        cleanup logic after the main `__work__` loop has been requested
        to stop but before background tasks are fully cancelled and awaited.
        It can be a regular method or an async method.

        Returns:
            Coroutine[Any, Any, None] | None: An awaitable if async logic is needed,
                                               otherwise None.
        """
        return None


class ServiceFn(AbstractService):
    """
    Concrete implementation of AbstractService that uses a provided asynchronous
    function as its main work loop.

    This allows creating simple services directly from an async function without
    needing to define a full class.
    """

    __work_fn__: Callable[[], Coroutine[Any, Any, None]]

    def __init__(
        self, fn: Callable[[], Coroutine[Any, Any, None]], *, name: Optional[str] = None
    ) -> None:
        """
        Initialize the ServiceFn instance.

        Args:
            fn (Callable[[], Coroutine[Any, Any, None]]): The asynchronous function
                that will serve as the main work loop (`__work__` method).
            name (Optional[str]): An optional name for the service. If None,
                                  the name of the provided function (`fn.__name__`)
                                  is used.
        """
        super().__init__(name=name or fn.__name__)
        self.__work_fn__ = fn

    def __work__(self) -> Coroutine[Any, Any, None]:
        """
        Execute one cycle of the service's work by calling the wrapped function.

        This method simply calls the asynchronous function provided during
        initialization (`self.__work_fn__`).

        Returns:
            Coroutine[Any, Any, None]: An awaitable representing the execution
                                       of the wrapped function.
        """
        return self.__work_fn__()


def service(
    *, name: Optional[str] = None
) -> Callable[[Callable[[], Coroutine[Any, Any, None]]], AbstractService]:
    """
    Decorator factory to create an AbstractService from an async function.

    Args:
        name (Optional[str]): An optional name for the service. If None,
                              the name of the decorated function will be used.

    Returns:
        Callable[[Callable[[], Coroutine[Any, Any, None]]], AbstractService]:
            A decorator function that takes an async function and returns
            an AbstractService instance.
    """

    def wrapper(func: Callable[[], Coroutine[Any, Any, None]]) -> AbstractService:
        """
        Decorator that transforms an async function into a ServiceFn instance.

        Args:
            func (Callable[[], Coroutine[Any, Any, None]]): The asynchronous
                function to be used as the service's main work loop.

        Returns:
            AbstractService: An instance of ServiceFn configured with the
                             provided function and name.
        """
        return ServiceFn(func, name=name)

    return wrapper
