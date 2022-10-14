import threading
from typing import Any, Callable, TypeVar, cast

from .event import Event
from .executor import Executor
from .scheduler import Scheduler

Callback = Callable[..., Any]
Number = TypeVar("Number", int, float)
EventType = TypeVar("EventType", bound=Event)


class Interval(Event):
    pass


class Timeout(Event):
    pass


class Timers:
    def __init__(self, executor: Executor | None = None) -> None:
        self._scheduler = Scheduler(executor)
        self._thread = threading.Thread(target=self._scheduler.run)

    def _set_event(self, event: EventType) -> EventType:
        ret_event = cast(EventType, self._scheduler.enter(event))

        if not self._thread.is_alive():
            self._thread = threading.Thread(target=self._scheduler.run)
            self._thread.start()

        return ret_event

    def _clear_event(self, event: EventType) -> None:
        self._scheduler.cancel(event)

        if self._scheduler.empty():
            self._scheduler.stop()

    def clear_interval(self, interval: Interval) -> None:
        self._clear_event(interval)

    def set_interval(self, callback: Callback, delay: Number = 0, *args) -> Interval:
        event = Interval(float(delay), True, callback, *args)

        return self._set_event(event)

    def clear_timeout(self, timeout: Timeout) -> None:
        self._clear_event(timeout)

    def set_timeout(self, callback: Callback, delay: Number = 0, *args) -> Timeout:
        event = Timeout(float(delay), False, callback, *args)

        return self._set_event(event)
