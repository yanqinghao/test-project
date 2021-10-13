# -*- coding: utf-8 -*-

from types import TracebackType
from typing import (
    TYPE_CHECKING,
    Any,
    List,
    ClassVar,
    ContextManager,
    Generic,
    MutableSequence,
    Optional,
    Type,
    TypeVar,
    Union,
)

from simpy.core import BoundClass, Environment
from simpy.events import Event, Process
from simpy.resources.base import BaseResource

ResourceType = TypeVar('ResourceType', bound='BaseResource')


class Put(Event, ContextManager['Put'], Generic[ResourceType]):
    """Generic event for requesting to put something into the *resource*.

    This event (and all of its subclasses) can act as context manager and can
    be used with the :keyword:`with` statement to automatically cancel the
    request if an exception (like an :class:`simpy.exceptions.Interrupt` for
    example) occurs:

    .. code-block:: python

        with res.put(item) as request:
            yield request

    """

    def __init__(self, resource: ResourceType):
        super().__init__(resource._env)
        self.resource = resource
        self.proc: Optional[Process] = self.env.active_process

        resource.put_queue.append(self)
        self.callbacks.append(resource._trigger_get)
        self.callbacks.append(resource._trigger_peek)
        resource._trigger_put(None)

    def __enter__(self) -> 'Put':
        return self

    def __exit__(
        self,
        exc_type: Optional[Type[BaseException]],
        exc_value: Optional[BaseException],
        traceback: Optional[TracebackType],
    ) -> Optional[bool]:
        self.cancel()
        return None

    def cancel(self) -> None:
        """Cancel this put request.

        This method has to be called if the put request must be aborted, for
        example if a process needs to handle an exception like an
        :class:`~simpy.exceptions.Interrupt`.

        If the put request was created in a :keyword:`with` statement, this
        method is called automatically.

        """
        if not self.triggered:
            self.resource.put_queue.remove(self)


class Get(Event, ContextManager['Get'], Generic[ResourceType]):
    """Generic event for requesting to get something from the *resource*.

    This event (and all of its subclasses) can act as context manager and can
    be used with the :keyword:`with` statement to automatically cancel the
    request if an exception (like an :class:`simpy.exceptions.Interrupt` for
    example) occurs:

    .. code-block:: python

        with res.get() as request:
            item = yield request

    """

    def __init__(self, resource: ResourceType):
        super().__init__(resource._env)
        self.resource = resource
        self.proc = self.env.active_process

        resource.get_queue.append(self)
        self.callbacks.append(resource._trigger_get_triggered)
        resource._trigger_get(None)

    def __enter__(self) -> 'Get':
        return self

    def __exit__(
        self,
        exc_type: Optional[Type[BaseException]],
        exc_value: Optional[BaseException],
        traceback: Optional[TracebackType],
    ) -> Optional[bool]:
        self.cancel()
        return None

    def cancel(self) -> None:
        """Cancel this get request.

        This method has to be called if the get request must be aborted, for
        example if a process needs to handle an exception like an
        :class:`~simpy.exceptions.Interrupt`.

        If the get request was created in a :keyword:`with` statement, this
        method is called automatically.

        """
        if not self.triggered:
            self.resource.get_queue.remove(self)


class Peek(Event, ContextManager['Peek'], Generic[ResourceType]):
    """Generic event for requesting to get something from the *resource*.

    This event (and all of its subclasses) can act as context manager and can
    be used with the :keyword:`with` statement to automatically cancel the
    request if an exception (like an :class:`simpy.exceptions.Interrupt` for
    example) occurs:

    .. code-block:: python

        with res.get() as request:
            item = yield request

    """

    def __init__(self, resource: ResourceType):
        super().__init__(resource._env)
        self.resource = resource
        self.proc = self.env.active_process

        resource.peek_queue.append(self)
        # self.callbacks.append(resource._trigger_get)
        resource._trigger_peek(None)

    def __enter__(self) -> 'Peek':
        return self

    def __exit__(
        self,
        exc_type: Optional[Type[BaseException]],
        exc_value: Optional[BaseException],
        traceback: Optional[TracebackType],
    ) -> Optional[bool]:
        self.cancel()
        return None

    def cancel(self) -> None:
        """Cancel this get request.

        This method has to be called if the get request must be aborted, for
        example if a process needs to handle an exception like an
        :class:`~simpy.exceptions.Interrupt`.

        If the get request was created in a :keyword:`with` statement, this
        method is called automatically.

        """
        if not self.triggered:
            self.resource.peek_queue.remove(self)


class GetTriggered(Event, ContextManager['GetTriggered'],
                   Generic[ResourceType]):
    """Generic event for requesting to get something from the *resource*.

    This event (and all of its subclasses) can act as context manager and can
    be used with the :keyword:`with` statement to automatically cancel the
    request if an exception (like an :class:`simpy.exceptions.Interrupt` for
    example) occurs:

    .. code-block:: python

        with res.get() as request:
            item = yield request

    """

    def __init__(self, resource: ResourceType):
        super().__init__(resource._env)
        self.resource = resource
        self.proc = self.env.active_process

        resource.get_triggered_queue.append(self)
        self.callbacks.append(resource._trigger_put)
        resource._trigger_get_triggered(None)

    def __enter__(self) -> 'Peek':
        return self

    def __exit__(
        self,
        exc_type: Optional[Type[BaseException]],
        exc_value: Optional[BaseException],
        traceback: Optional[TracebackType],
    ) -> Optional[bool]:
        self.cancel()
        return None

    def cancel(self) -> None:
        """Cancel this get request.

        This method has to be called if the get request must be aborted, for
        example if a process needs to handle an exception like an
        :class:`~simpy.exceptions.Interrupt`.

        If the get request was created in a :keyword:`with` statement, this
        method is called automatically.

        """
        if not self.triggered:
            self.resource.get_triggered_queue.remove(self)


PutType = TypeVar('PutType', bound=Put)
GetType = TypeVar('GetType', bound=Get)
PeekType = TypeVar('PeekType', bound=Peek)
GetTriggeredType = TypeVar('GetTriggeredType', bound=GetTriggered)


class StorePut(Put):
    """Request to put *item* into the *store*. The request is triggered once
    there is space for the item in the store.

    """

    def __init__(self, store: 'Store', item: Any):
        self.item = item
        """The item to put into the store."""
        super().__init__(store)


class StoreGet(Get):
    """Request to get an *item* from the *store*. The request is triggered
    once there is an item available in the store.

    """


class StorePeek(Peek):
    """Request to get an *item* from the *store*. The request is triggered
    once there is an item available in the store.

    """


class StoreGetTriggered(GetTriggered):
    """Request to get an *item* from the *store*. The request is triggered
    once there is an item available in the store.

    """


class Store(BaseResource):
    """Resource with *capacity* slots for storing arbitrary objects. By
    default, the *capacity* is unlimited and objects are put and retrieved from
    the store in a first-in first-out order.

    The *env* parameter is the :class:`~simpy.core.Environment` instance the
    container is bound to.

    """
    PeekQueue: ClassVar[Type[MutableSequence[PeekType]]] = list
    GetTriggeredQueue: ClassVar[Type[MutableSequence[GetTriggeredType]]] = list
    """The type to be used for the :attr:`get_queue`. It is a plain
    :class:`list` by default. The type must support index access (e.g.
    ``__getitem__()`` and ``__len__()``) as well as provide ``append()`` and
    ``pop()`` operations."""

    def __init__(self,
                 env: Environment,
                 capacity: Union[float, int] = float('inf')):
        if capacity <= 0:
            raise ValueError('"capacity" must be > 0.')
        self.peek_queue = self.PeekQueue()
        self.get_triggered_queue = self.GetTriggeredQueue()
        super().__init__(env, capacity)
        self.items: List[Any] = []
        """List of the items available in the store."""

    if TYPE_CHECKING:

        def put(  # type: ignore[override] # noqa: F821
                self, item: Any) -> StorePut:
            """Request to put *item* into the store."""
            return StorePut(self, item)

        def get(self) -> StoreGet:  # type: ignore[override] # noqa: F821
            """Request to get an *item* out of the store."""
            return StoreGet(self)

        def peek(self) -> StorePeek:
            return StorePeek(self)

        def get_triggered(self) -> StoreGetTriggered:
            return StoreGetTriggered(self)

    else:
        put = BoundClass(StorePut)
        get = BoundClass(StoreGet)
        peek = BoundClass(StorePeek)
        get_triggered = BoundClass(StoreGetTriggered)

    def _do_put(self, event: StorePut) -> Optional[bool]:
        if len(self.items) < self._capacity:
            self.items.append(event.item)
            event.succeed(True)
        return None

    def _do_get(self, event: StoreGet) -> Optional[bool]:
        if self.items:
            event.succeed(self.items.pop(0))
        return None

    def _do_peek(self, event: StorePeek) -> Optional[bool]:
        if self.items:
            event.succeed(self.items[0])
        return None

    def _do_get_triggered(self, event: StoreGetTriggered) -> Optional[bool]:
        if not self.items:
            event.succeed(True)
        return None

    def _trigger_peek(self, put_event: Optional[PutType]) -> None:
        """Trigger get events.

        This method is called once a new get event has been created or a put
        event has been processed.

        The method iterates over all get events in the :attr:`get_queue` and
        calls :meth:`_do_get` to check if the conditions for the event are met.
        If :meth:`_do_get` returns ``False``, the iteration is stopped early.
        """

        # Maintain queue invariant: All get requests must be untriggered.
        # This code is not very pythonic because the queue interface should be
        # simple (only append(), pop(), __getitem__() and __len__() are
        # required).
        idx = 0
        while idx < len(self.peek_queue):
            peek_event = self.peek_queue[idx]
            proceed = self._do_peek(peek_event)
            if not peek_event.triggered:
                idx += 1
            elif self.peek_queue.pop(idx) != peek_event:
                raise RuntimeError('Get queue invariant violated')

            if not proceed:
                break

    def _trigger_get_triggered(self, get_event: Optional[GetType]) -> None:
        """Trigger get events.

        This method is called once a new get event has been created or a put
        event has been processed.

        The method iterates over all get events in the :attr:`get_queue` and
        calls :meth:`_do_get` to check if the conditions for the event are met.
        If :meth:`_do_get` returns ``False``, the iteration is stopped early.
        """

        # Maintain queue invariant: All get requests must be untriggered.
        # This code is not very pythonic because the queue interface should be
        # simple (only append(), pop(), __getitem__() and __len__() are
        # required).
        idx = 0
        while idx < len(self.get_triggered_queue):
            get_triggered_event = self.get_triggered_queue[idx]
            proceed = self._do_get_triggered(get_triggered_event)
            if not get_triggered_event.triggered:
                idx += 1
            elif self.get_triggered_queue.pop(idx) != get_triggered_event:
                raise RuntimeError('Get queue invariant violated')

            if not proceed:
                break

    def _trigger_put(self, get_event: Optional[GetType]) -> None:
        """This method is called once a new put event has been created or a get
        event has been processed.

        The method iterates over all put events in the :attr:`put_queue` and
        calls :meth:`_do_put` to check if the conditions for the event are met.
        If :meth:`_do_put` returns ``False``, the iteration is stopped early.
        """

        # Maintain queue invariant: All put requests must be untriggered.
        # This code is not very pythonic because the queue interface should be
        # simple (only append(), pop(), __getitem__() and __len__() are
        # required).
        idx = 0
        while idx < len(self.put_queue):
            put_event = self.put_queue[idx]
            proceed = self._do_put(put_event)
            if not put_event.triggered:
                idx += 1
            elif self.put_queue.pop(idx) != put_event:
                raise RuntimeError('Put queue invariant violated')

            if not proceed:
                break

    def _trigger_get(self, put_event: Optional[PutType]) -> None:
        """Trigger get events.

        This method is called once a new get event has been created or a put
        event has been processed.

        The method iterates over all get events in the :attr:`get_queue` and
        calls :meth:`_do_get` to check if the conditions for the event are met.
        If :meth:`_do_get` returns ``False``, the iteration is stopped early.
        """

        # Maintain queue invariant: All get requests must be untriggered.
        # This code is not very pythonic because the queue interface should be
        # simple (only append(), pop(), __getitem__() and __len__() are
        # required).
        idx = 0
        while idx < len(self.get_queue):
            get_event = self.get_queue[idx]
            proceed = self._do_get(get_event)
            if not get_event.triggered:
                idx += 1
            elif self.get_queue.pop(idx) != get_event:
                raise RuntimeError('Get queue invariant violated')

            if not proceed:
                break
