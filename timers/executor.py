from concurrent.futures import Executor, Future
from typing import Any, Callable


class BasicExecutor(Executor):
    """
    Executes the given function immediately on the current thread.
    """

    def submit(self, fn: Callable[..., Any], /, *args: Any, **kwargs: Any) -> Future:
        future: Future = Future()

        try:
            result = fn(*args, **kwargs)
        except BaseException as exc:
            future.set_exception(exc)
        else:
            future.set_result(result)

        return future
