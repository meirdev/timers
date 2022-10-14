from typing import Any, Callable, TypeVar

Self = TypeVar("Self", bound="Event")


class Event:
    def __init__(
        self, delay: float, repeat: bool, fn: Callable[..., Any], /, *args: Any
    ) -> None:
        self.delay = delay
        self.repeat = repeat
        self.fn = fn
        self.args = args

        self.time: float = 0.0

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Event):
            return NotImplemented

        return self.time == other.time

    def __lt__(self, other: Self) -> bool:
        return self.time < other.time

    def __le__(self, other: Self) -> bool:
        return self.time <= other.time

    def __gt__(self, other: Self) -> bool:
        return self.time > other.time

    def __ge__(self, other: Self) -> bool:
        return self.time >= other.time
