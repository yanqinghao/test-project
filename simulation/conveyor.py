# -*- coding: utf-8 -*-

import pdb
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
from simpy.resources.base import BaseResource, GetType

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
        # self.callbacks.append(resource._trigger_put)
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


class Pop(Event, ContextManager['Pop'], Generic[ResourceType]):
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

        resource.pop_queue.append(self)
        self.callbacks.append(resource._trigger_get_triggered)
        resource._trigger_pop(None)

    def __enter__(self) -> 'Pop':
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
            self.resource.pop_queue.remove(self)


class Push(Event, ContextManager['Push'], Generic[ResourceType]):
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

        resource.push_queue.append(self)
        self.callbacks.append(resource._trigger_pop)
        resource._trigger_push(None)

    def __enter__(self) -> 'Push':
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
            self.resource.push_queue.remove(self)


PutType = TypeVar('PutType', bound=Put)
PeekType = TypeVar('PeekType', bound=Peek)
GetTriggeredType = TypeVar('GetTriggeredType', bound=GetTriggered)
PopType = TypeVar('PopType', bound=Pop)
PushType = TypeVar('PushType', bound=Push)


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
    def __init__(self, store: 'Store', item: Any):
        self.item = item
        """The item to put into the store."""
        super().__init__(store)


class StorePeek(Peek):
    """Request to get an *item* from the *store*. The request is triggered
    once there is an item available in the store.

    """


class StoreGetTriggered(GetTriggered):
    """Request to get an *item* from the *store*. The request is triggered
    once there is an item available in the store.

    """


class StorePop(Pop):
    """Request to get an *item* from the *store*. The request is triggered
    once there is an item available in the store.

    """


class StorePush(Push):
    """Request to get an *item* from the *store*. The request is triggered
    once there is an item available in the store.

    """
    def __init__(self, store: 'Store', item: Any):
        self.item = item
        """The item to put into the store."""
        super().__init__(store)


class Store(BaseResource):
    """Resource with *capacity* slots for storing arbitrary objects. By
    default, the *capacity* is unlimited and objects are put and retrieved from
    the store in a first-in first-out order.

    The *env* parameter is the :class:`~simpy.core.Environment` instance the
    container is bound to.

    """
    PeekQueue: ClassVar[Type[MutableSequence[PeekType]]] = list
    GetTriggeredQueue: ClassVar[Type[MutableSequence[GetTriggeredType]]] = list
    PopQueue: ClassVar[Type[MutableSequence[PopType]]] = list
    PushQueue: ClassVar[Type[MutableSequence[PushType]]] = list
    """The type to be used for the :attr:`get_queue`. It is a plain
    :class:`list` by default. The type must support index access (e.g.
    ``__getitem__()`` and ``__len__()``) as well as provide ``append()`` and
    ``pop()`` operations."""
    def __init__(self,
                 env: Environment,
                 capacity: int = -1,
                 length: int = 2,
                 speed: int = 1,
                 acceleration: int = 0,
                 deceleration: int = 0,
                 distance: int = -1):
        super().__init__(env, capacity)
        self.peek_queue = self.PeekQueue()
        self.get_triggered_queue = self.GetTriggeredQueue()
        self.pop_queue = self.PopQueue()
        self.push_queue = self.PushQueue()

        self.length = length
        self.speed = speed
        self.acceleration = acceleration
        self.deceleration = deceleration
        self.distance = distance
        self.items: List[Any] = []
        """List of the items available in the store."""
        self.processing_queue: List[Any] = []
        self.ready_queue: List[Any] = []
        """List of the items available in the store."""

    if TYPE_CHECKING:

        def put(  # type: ignore[override] # noqa: F821
                self, item: Any) -> StorePut:
            """Request to put *item* into the store."""
            return StorePut(self, item)

        def get(self,
                item: Any) -> StoreGet:  # type: ignore[override] # noqa: F821
            """Request to get an *item* out of the store."""
            return StoreGet(self, item)

        def peek(self) -> StorePeek:
            return StorePeek(self)

        def get_triggered(self) -> StoreGetTriggered:
            return StoreGetTriggered(self)

        def pop(self) -> StorePop:
            return StorePop(self)

        def push(self) -> StorePush:
            return StorePush(self)

    else:
        put = BoundClass(StorePut)
        get = BoundClass(StoreGet)
        peek = BoundClass(StorePeek)
        get_triggered = BoundClass(StoreGetTriggered)
        pop = BoundClass(StorePop)
        push = BoundClass(StorePush)

    def _get_duration(self):
        return self.length / self.speed

    def _check_distance(self):
        if self.distance == -1:
            return 0
        elif len(self.processing_queue) == 0:
            return 0
        else:
            return (self.distance -
                    (self._env.now - self.processing_queue[-1]["startTime"]) *
                    self.speed) / self.speed

    def _check_capacity(self):
        if self.capacity == -1:
            return 0
        elif len(self.processing_queue) < self.capacity:
            return 0
        else:
            return self._get_duration() - (
                self._env.now - self.processing_queue[0]["startTime"])

    def _capacity_available(self):
        if self.capacity == -1:
            return True
        elif len(self.processing_queue) < self.capacity:
            return True
        else:
            return False

    def _check_available(self):
        return self._check_distance() <= 0 and self._check_capacity(
        ) <= 0 and self._capacity_available()

    def _do_put(self, event: StorePut) -> Optional[bool]:
        if self._check_available():
            self.processing_queue.append({
                "data": event.item,
                "startTime": self._env.now
            })
            event.succeed(True)
        return None

    def _do_get(self, event: StoreGet) -> Optional[bool]:
        if self.processing_queue[event.item]:
            event.succeed(self.processing_queue[event.item])
        return None

    def _do_peek(self, event: StorePeek) -> Optional[bool]:
        if self.items:
            event.succeed(self.items[0])
        return None

    def _do_get_triggered(self, event: StoreGetTriggered) -> Optional[bool]:
        if self._check_available():
            event.succeed(True)
        return None

    def _do_pop(self, event: StorePop) -> Optional[bool]:
        if self.ready_queue:
            event.succeed(self.ready_queue.pop(0))
            self.processing_queue.pop(0)
        return None

    def _do_push(self, event: StorePush) -> Optional[bool]:
        self.ready_queue.append(event.item)
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

    def _trigger_pop(self, get_event: Optional[GetType]) -> None:
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
        while idx < len(self.pop_queue):
            pop_event = self.pop_queue[idx]
            proceed = self._do_pop(pop_event)
            if not pop_event.triggered:
                idx += 1
            elif self.pop_queue.pop(idx) != pop_event:
                raise RuntimeError('Get queue invariant violated')

            if not proceed:
                break

    def _trigger_push(self, get_event: Optional[GetType]) -> None:
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
        while idx < len(self.push_queue):
            push_event = self.push_queue[idx]
            proceed = self._do_push(push_event)
            if not push_event.triggered:
                idx += 1
            elif self.push_queue.pop(idx) != push_event:
                raise RuntimeError('Get queue invariant violated')

            if not proceed:
                break
