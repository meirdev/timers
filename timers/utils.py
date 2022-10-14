import asyncio
import functools
from typing import Awaitable, Callable, ParamSpec, TypeVar

P = ParamSpec("P")
R = TypeVar("R")


def async_to_sync(fn: Callable[P, Awaitable[R]]) -> Callable[P, R]:
    @functools.wraps(fn)
    def inner(*args: P.args, **kwargs: P.kwargs) -> R:
        return asyncio.run(fn(*args, **kwargs))

    return inner


is_async = asyncio.iscoroutinefunction
