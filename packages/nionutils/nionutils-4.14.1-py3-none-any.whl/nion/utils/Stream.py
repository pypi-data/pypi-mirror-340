"""
Classes related to streams of values, used for reactive style programming.
"""
from __future__ import annotations

# standard libraries
import asyncio
import contextlib
import enum
import operator
import types
import typing

# third party libraries
# None

# local libraries
import weakref

from . import Event
from . import Observable
from .ReferenceCounting import weak_partial

T = typing.TypeVar('T', covariant=True)
OT = typing.TypeVar('OT', covariant=True)
EqualityOperator = typing.Callable[[typing.Any, typing.Any], bool]

RefT = typing.TypeVar('RefT', covariant=True)

class AbstractStream(typing.Generic[T]):
    """A stream provides a value property and a value_stream event that fires when the value changes."""

    def __init__(self) -> None:
        super().__init__()
        self.value_stream = typing.cast(Event.Event, None)

    @property
    def value(self) -> typing.Optional[T]:
        return None

    def about_to_delete(self) -> None:
        pass

    def add_ref(self) -> AbstractStream[T]:
        return self

    def remove_ref(self, check: bool = True) -> None:
        pass

    class RefContextManager(typing.Generic[RefT]):
        def __init__(self, item: AbstractStream[RefT]) -> None:
            self.__item = item

        def __enter__(self) -> AbstractStream[RefT]:
            return self.__item

        def __exit__(self, exception_type: typing.Optional[typing.Type[BaseException]],
                     value: typing.Optional[BaseException], traceback: typing.Optional[types.TracebackType]) -> typing.Optional[bool]:
            return None

    def ref(self) -> contextlib.AbstractContextManager[AbstractStream[T]]:
        return AbstractStream.RefContextManager(self)


class StreamTask:

    def __init__(self, task: typing.Optional[typing.Coroutine[typing.Any, typing.Any, typing.Any]], event_loop: typing.Optional[asyncio.AbstractEventLoop]) -> None:
        self.__task: typing.Optional[asyncio.Task[None]] = None
        self.__event_loop = event_loop or asyncio.get_running_loop()
        if task:
            self.create_task(task)

    def clear(self) -> None:
        if self.__task:
            self.__task.cancel()
        self.__task = None

    @property
    def is_active(self) -> bool:
        return self.__task is not None

    def create_task(self, task: typing.Coroutine[typing.Any, typing.Any, typing.Any]) -> asyncio.Task[None]:
        assert self.__task is None
        self.__task = self.__event_loop.create_task(task)

        def zero_task(t: asyncio.Task[None]) -> None:
            self.__task = None

        self.__task.add_done_callback(zero_task)
        return self.__task


class ValueStream(AbstractStream[T], typing.Generic[T]):
    """A stream that sends out value when value is set."""

    def __init__(self, value: typing.Optional[T] = None, cmp: typing.Optional[EqualityOperator] = None) -> None:
        super().__init__()
        # internal values
        self.__value = value
        self.__cmp = cmp if cmp else operator.eq
        # outgoing messages
        self.value_stream = Event.Event()

    def add_ref(self) -> ValueStream[T]:
        return self

    @property
    def value(self) -> typing.Optional[T]:
        return self.__value

    @value.setter
    def value(self, value: typing.Optional[T]) -> None:
        if not self.__cmp(value, self.__value):
            self.send_value(value)

    def send_value(self, value: typing.Optional[T]) -> None:
        self.__value = value
        self._send_value()

    def _send_value(self) -> None:
        """Subclasses may override this to filter or modify."""
        self.value_stream.fire(self.value)


class MapStream(AbstractStream[OT], typing.Generic[T, OT]):
    """A stream that applies a function when input streams change."""

    def __init__(self, stream: AbstractStream[T], value_fn: typing.Callable[[typing.Optional[T]], typing.Optional[OT]]) -> None:
        super().__init__()
        # outgoing messages
        self.value_stream = Event.Event()
        # references
        self.__stream = stream
        # initialize values
        self.__value: typing.Optional[OT] = None

        # listen for display changes
        def update_value(stream: MapStream[T, OT], value: typing.Optional[T]) -> None:
            new_value = value_fn(value)
            if new_value != stream.value:
                stream.send_value(new_value)

        # use weak_partial to avoid holding references to self.
        self.__listener = stream.value_stream.listen(weak_partial(update_value, self))
        update_value(self, stream.value)

    @property
    def value(self) -> typing.Optional[OT]:
        return self.__value

    def send_value(self, value: typing.Optional[OT]) -> None:
        self.__value = value
        self.value_stream.fire(self.value)


class CombineLatestStream(AbstractStream[OT], typing.Generic[T, OT]):
    """A stream that produces a tuple of values when input streams change."""

    def __init__(self, stream_list: typing.Sequence[AbstractStream[T]],
                 value_fn: typing.Optional[typing.Callable[..., typing.Optional[OT]]] = None) -> None:
        super().__init__()
        # outgoing messages
        self.value_stream = Event.Event()
        # references
        self.__stream_list: typing.List[AbstractStream[T]] = list()
        self.__value_fn = value_fn or (lambda *x: typing.cast(OT, tuple(x)))
        # initialize values
        self.__values: typing.List[typing.Optional[T]] = list()
        self.__value: typing.Optional[OT] = None
        # listen for display changes
        self.__listeners: typing.List[Event.EventListener] = list()
        for stream in stream_list:
            self.__stream_list.append(stream)
            self.__listeners.append(stream.value_stream.listen(weak_partial(CombineLatestStream.__handle_stream_value, self, stream)))
            self.__values.append(stream.value)
        self.__values_changed()

    def append_stream(self, stream: AbstractStream[T]) -> None:
        self.insert_stream(len(self.__stream_list), stream)

    def insert_stream(self, index: int, stream: AbstractStream[T]) -> None:
        self.__stream_list.insert(index, stream)
        self.__listeners.insert(index, stream.value_stream.listen(weak_partial(CombineLatestStream.__handle_stream_value, self, stream)))
        self.__values.insert(index, stream.value)
        self.__values_changed()

    def remove_stream(self, index: int) -> None:
        self.__stream_list.pop(index)
        self.__listeners.pop(index)
        self.__values.pop(index)
        self.__values_changed()

    def replace_stream(self, index: int, stream: AbstractStream[T]) -> None:
        self.__stream_list[index] = stream
        self.__listeners[index] = stream.value_stream.listen(weak_partial(CombineLatestStream.__handle_stream_value, self, stream))
        self.__values[index] = stream.value
        self.__values_changed()

    @property
    def stream_list(self) -> typing.Sequence[AbstractStream[T]]:
        return self.__stream_list

    def __handle_stream_value(self, stream: AbstractStream[T], value: typing.Optional[T]) -> None:
        index = self.__stream_list.index(stream)
        self.__values[index] = value
        self.__values_changed()

    def __values_changed(self) -> None:
        self.__value = self.__value_fn(*self.__values)
        self.value_stream.fire(self.__value)

    @property
    def value(self) -> typing.Optional[OT]:
        return self.__value


class DebounceValue(typing.Generic[T]):
    def __init__(self) -> None:
        self.value: typing.Optional[T] = None


class DebounceStream(AbstractStream[T], typing.Generic[T]):
    """A stream that produces the latest value after a specified interval has elapsed."""

    def __init__(self, input_stream: AbstractStream[T], period: float, event_loop: typing.Optional[asyncio.AbstractEventLoop]) -> None:
        super().__init__()
        self.value_stream = Event.Event()
        self.__input_stream = input_stream
        self.__period = period
        self.__value_holder = DebounceValue[T]()

        # define a stub and use weak_partial to avoid holding references to self.
        def value_changed(stream: DebounceStream[T], value: typing.Optional[T]) -> None:
            stream.__value_changed(value)

        self.__listener = input_stream.value_stream.listen(weak_partial(value_changed, self))
        self.__debounce_task = StreamTask(None, event_loop)
        self.__value_changed(input_stream.value)

        def finalize(task: StreamTask) -> None:
            task.clear()

        weakref.finalize(self, finalize, self.__debounce_task)

    def __value_changed(self, value: typing.Optional[T]) -> None:
        self.__value_holder.value = value
        if not self.__debounce_task.is_active:  # only trigger new task if necessary

            async def debounce_delay(period: float, value_stream: Event.Event, value_holder: DebounceValue[T]) -> None:
                await asyncio.sleep(period)
                value_stream.fire(value_holder.value)

            self.__debounce_task.create_task(debounce_delay(self.__period, self.value_stream, self.__value_holder))

    @property
    def value(self) -> typing.Optional[T]:
        return self.__value_holder.value


class SampleValue(typing.Generic[T]):
    def __init__(self) -> None:
        self.value: typing.Optional[T] = None
        self.pending_value: typing.Optional[T] = None
        self.is_dirty = False

    def set_pending_value(self, value: typing.Optional[T]) -> None:
        self.pending_value = value
        self.is_dirty = True


class SampleStream(AbstractStream[T], typing.Generic[T]):
    """A stream that produces new values at a specified interval."""

    def __init__(self, input_stream: AbstractStream[T], period: float, event_loop: typing.Optional[asyncio.AbstractEventLoop] = None) -> None:
        super().__init__()
        self.value_stream = Event.Event()
        self.__input_stream = input_stream
        self.__sample_value = SampleValue[T]()

        # define a stub and use weak_partial to avoid holding references to self.
        def value_changed(stream: SampleStream[T], value: typing.Optional[T]) -> None:
            stream.__value_changed(value)

        self.__listener = input_stream.value_stream.listen(weak_partial(value_changed, self))
        self.__sample_value.value = input_stream.value

        async def sample_loop(period: float, value_stream: Event.Event, sample_value: SampleValue[T]) -> typing.NoReturn:
            while True:
                await asyncio.sleep(period)
                if sample_value.is_dirty:
                    sample_value.value = sample_value.pending_value
                    sample_value.is_dirty = False
                    value_stream.fire(sample_value.value)

        self.__sample_task = StreamTask(sample_loop(period, self.value_stream, self.__sample_value), event_loop)

        def finalize(task: StreamTask) -> None:
            task.clear()

        weakref.finalize(self, finalize, self.__sample_task)

    def __value_changed(self, value: typing.Optional[T]) -> None:
        self.__sample_value.set_pending_value(value)

    @property
    def value(self) -> typing.Optional[T]:
        return self.__sample_value.value


class ConstantStream(AbstractStream[T], typing.Generic[T]):

    def __init__(self, value: typing.Optional[T]) -> None:
        super().__init__()
        self.__value = value
        self.value_stream = Event.Event()

    @property
    def value(self) -> typing.Optional[T]:
        return self.__value


class PropertyChangedEventStream(AbstractStream[T], typing.Generic[T]):
    """A stream generated from observing a property changed event of an Observable object."""

    # see https://rehansaeed.com/reactive-extensions-part2-wrapping-events/

    def __init__(self, source_object: typing.Union[Observable.Observable, AbstractStream[Observable.Observable]],
                 property_name: str, cmp: typing.Optional[EqualityOperator] = None) -> None:
        super().__init__()
        # outgoing messages
        self.value_stream = Event.Event()
        # references
        source_stream: AbstractStream[Observable.Observable]
        if not isinstance(source_object, AbstractStream):
            source_stream = ConstantStream[Observable.Observable](source_object)
        else:
            source_stream = source_object
        self.__source_stream = source_stream
        self.__source_object: typing.Optional[Observable.Observable] = None
        # initialize
        self.__property_name = property_name
        self.__value = None
        self.__cmp = cmp if cmp else operator.eq
        self.__property_changed_listener: typing.Optional[Event.EventListener] = None

        # define a stub and use weak_partial to avoid holding references to self.
        def source_object_changed(stream: PropertyChangedEventStream[T], source_object: typing.Optional[Observable.Observable]) -> None:
            stream.__source_object_changed(source_object)

        self.__source_stream_listener = self.__source_stream.value_stream.listen(weak_partial(source_object_changed, self))
        source_object_changed(self, self.__source_stream.value)

    @property
    def value(self) -> typing.Optional[T]:
        return self.__value

    def __source_object_changed(self, source_object: typing.Optional[Observable.Observable]) -> None:
        self.__property_changed_listener = None
        self.__source_object = source_object
        if self.__source_object:
            # define a stub and use weak_partial to avoid holding references to self.
            def property_changed(stream: PropertyChangedEventStream[T], key: str) -> None:
                stream.__property_changed(key)

            self.__property_changed_listener = self.__source_object.property_changed_event.listen(weak_partial(property_changed, self))
        self.__property_changed(self.__property_name)

    def __property_changed(self, key: str) -> None:
        if key == self.__property_name:
            new_value = getattr(self.__source_object, self.__property_name, None)
            if not self.__cmp(new_value, self.__value):
                self.__value = new_value
                self.value_stream.fire(self.__value)


class OptionalStream(ValueStream[T], typing.Generic[T]):
    """Sends value from input stream or None."""

    def __init__(self, stream: AbstractStream[T], pred: typing.Callable[[typing.Optional[T]], bool]) -> None:
        super().__init__()
        self.__stream = stream
        self.__pred = pred

        # define a stub and use weak_partial to avoid holding references to self.
        def value_changed(stream: OptionalStream[T], value: typing.Optional[T]) -> None:
            stream.__value_changed(value)

        self.__stream_listener = self.__stream.value_stream.listen(weak_partial(value_changed, self))
        self.value_stream = Event.Event()
        self.__value_changed(self.__stream.value)

    def __value_changed(self, value: typing.Optional[T]) -> None:
        if self.__pred(value):
            self.value = value
        else:
            self.value = None


class FollowStream(ValueStream[T], typing.Generic[T]):
    """Sends value from input stream. Input stream can be changed."""

    def __init__(self, stream: typing.Optional[AbstractStream[T]] = None) -> None:
        super().__init__()
        self.__stream: AbstractStream[T]
        self.__stream_action: ValueStreamAction[T]
        self.stream = stream

    @property
    def stream(self) -> typing.Optional[AbstractStream[T]]:
        return self.__stream

    @stream.setter
    def stream(self, stream: typing.Optional[AbstractStream[T]]) -> None:
        stream = stream or ConstantStream[T](None)
        self.__stream = stream
        self.__stream_action = ValueStreamAction(self.__stream, weak_partial(FollowStream.__value_changed, self))
        self.__value_changed(self.__stream.value)

    # define a stub and use weak_partial to avoid holding references to self.
    def __value_changed(self, value: typing.Optional[T]) -> None:
        self.value = value



class PrintStream:
    """Prints value from input stream."""

    def __init__(self, stream: AbstractStream[typing.Any]) -> None:
        super().__init__()
        self.__stream = stream

        # define a stub and use weak_partial to avoid holding references to self.
        def value_changed(stream: PrintStream, value: typing.Any) -> None:
            stream.__value_changed(value)

        self.__stream_listener = self.__stream.value_stream.listen(weak_partial(value_changed, self))

    def __value_changed(self, value: typing.Any) -> None:
        print(f"value={value}")


class ValueStreamAction(typing.Generic[T]):
    """Calls an action function when the stream value changes."""

    def __init__(self, stream: AbstractStream[T], fn: typing.Callable[[typing.Optional[T]], None]) -> None:
        super().__init__()
        self.__stream = stream

        # define a stub and use weak_partial to avoid holding references to self.
        def value_changed(a: ValueStreamAction[T], value: typing.Optional[T]) -> None:
            a.__value_changed(value)

        self.__stream_listener = self.__stream.value_stream.listen(weak_partial(value_changed, self))
        self.__fn = fn

    def close(self) -> None:
        pass

    def __value_changed(self, value: typing.Optional[T]) -> None:
        self.__fn(value)


class ValueChangeType(enum.IntEnum):
    BEGIN = 0
    CHANGE = 1
    END = 2


class ValueChange(typing.Generic[T]):
    def __init__(self, state: int, value: typing.Optional[T]) -> None:
        self.state = state
        self.value = value

    def __repr__(self) -> str:
        return f"{self.state}: {self.value}"

    @property
    def is_begin(self) -> bool:
        return self.state == ValueChangeType.BEGIN

    @property
    def is_end(self) -> bool:
        return self.state == ValueChangeType.END


class ValueChangeStream(ValueStream[ValueChange[T]], typing.Generic[T]):
    def __init__(self, value_stream: AbstractStream[T]) -> None:
        super().__init__()
        self.__value_stream = value_stream
        self.__value_stream_listener = self.__value_stream.value_stream.listen(weak_partial(ValueChangeStream.__value_changed, self))
        self.__is_active = False

    def add_ref(self) -> ValueChangeStream[T]:
        return self

    def _send_value(self) -> None:
        if self.__is_active:
            assert self.value is not None
            super()._send_value()

    def begin(self) -> None:
        self.__is_active = True
        self.value = ValueChange(ValueChangeType.BEGIN, self.__value_stream.value)

    def end(self) -> None:
        self.value = ValueChange(ValueChangeType.END, self.__value_stream.value)
        self.__is_active = False

    def __value_changed(self, value: typing.Optional[T]) -> None:
        self.value = ValueChange(ValueChangeType.CHANGE, self.__value_stream.value)


ValueChangeStreamReactorInterfaceT = typing.TypeVar("ValueChangeStreamReactorInterfaceT", covariant=True)


class ValueChangeStreamReactorInterface(typing.Protocol[ValueChangeStreamReactorInterfaceT]):
    async def next_value_change(self) -> ValueChange[ValueChangeStreamReactorInterfaceT]: ...


class ValueChangeStreamReactor(typing.Generic[T]):
    def __init__(self, value_change_stream: ValueChangeStream[T], cfn: typing.Callable[[ValueChangeStreamReactorInterface[T]], typing.Coroutine[typing.Any, typing.Any, typing.Any]], event_loop: typing.Optional[asyncio.AbstractEventLoop] = None) -> None:
        self.__value_change_stream = value_change_stream
        self.__cfn = cfn
        self.__event_loop = event_loop or asyncio.get_running_loop()
        self.__value_changed_listener = value_change_stream.value_stream.listen(weak_partial(ValueChangeStreamReactor.__value_changed, self))
        self.__event_queue: asyncio.Queue[ValueChange[T]] = asyncio.Queue()
        self.__task: typing.Optional[asyncio.Task[None]] = None
        self.__had_exception = False

    def __value_changed(self, value_change: ValueChange[T]) -> None:
        if value_change.state == ValueChangeType.BEGIN:
            self.__had_exception = False
            self.__event_queue.put_nowait(value_change)  # ensure loop gets the begin event
            self.run()
        elif not self.__had_exception:
            self.__event_queue.put_nowait(value_change)

    def run(self) -> None:
        class AValueChangeStreamReactor(ValueChangeStreamReactorInterface[T]):
            def __init__(self, event_queue: asyncio.Queue[ValueChange[T]]) -> None:
                self.__event_queue = event_queue

            async def next_value_change(self) -> ValueChange[typing.Any]:
                r = await self.__event_queue.get()
                self.__event_queue.task_done()
                return r

        async def run_task(cfn: typing.Callable[[ValueChangeStreamReactorInterface[T]], typing.Coroutine[typing.Any, typing.Any, typing.Any]], event_queue: asyncio.Queue[ValueChange[T]]) -> None:
            try:
                await cfn(AValueChangeStreamReactor(event_queue))
            except Exception:
                self.__had_exception = True

        self.__task = self.__event_loop.create_task(run_task(self.__cfn, self.__event_queue))

        def finalize(task: typing.Optional[asyncio.Task[None]]) -> None:
            if task:
                task.cancel()

        weakref.finalize(self, finalize, self.__task)

    async def next_value_change(self) -> ValueChange[T]:
        return await self.__event_queue.get()
