import heapq
import threading
import time

from .event import Event
from .executor import BasicExecutor, Executor
from .utils import async_to_sync, is_async

basic_executor = BasicExecutor()


class Scheduler:
    def __init__(self, executor: Executor | None = None) -> None:
        self._executor = executor or basic_executor
        self._lock = threading.RLock()
        self._cond = threading.Condition()
        self._queue: list[Event] = []

    @property
    def queue(self) -> list[Event]:
        return self._queue

    def cancel(self, event: Event) -> None:
        with self._lock:
            if event in self._queue:
                self._queue.remove(event)
            heapq.heapify(self._queue)

    def empty(self) -> bool:
        with self._lock:
            return not self._queue

    def enter(self, event: Event) -> Event:
        with self._lock:
            event.time = time.time() + event.delay
            heapq.heappush(self._queue, event)

        with self._cond:
            self._cond.notify()

        return event

    def stop(self) -> None:
        with self._lock:
            self._queue.clear()

        with self._cond:
            self._cond.notify()

    def run(self) -> None:
        with self._executor as executor_:
            while True:
                with self._lock:
                    if not self._queue:
                        break

                    event = self._queue[0]
                    now = time.time()

                    if event.time > now:
                        delay = True
                    else:
                        delay = False
                        heapq.heappop(self._queue)

                if delay:
                    with self._cond:
                        self._cond.wait(event.time - now)
                else:
                    if is_async(event.fn):
                        executor_.submit(async_to_sync(event.fn)(*event.args))
                    else:
                        executor_.submit(event.fn, *event.args)

                    time.sleep(0)

                    if event.repeat:
                        self.enter(event)
