import time

from timers import clear_interval, clear_timeout, set_interval, set_timeout


class Foo:
    @classmethod
    def bar(cls):
        pass

    @classmethod
    async def async_bar(cls):
        pass


def test_set_interval(mocker):
    foo = Foo()
    spy = mocker.spy(foo, "bar")

    i = set_interval(foo.bar, 2)

    time.sleep(2.2)
    assert spy.call_count == 1

    time.sleep(2.2)
    assert spy.call_count == 2

    time.sleep(2.2)
    assert spy.call_count == 3

    clear_interval(i)


def test_set_timeout(mocker):
    foo = Foo()
    spy = mocker.spy(foo, "bar")

    i = set_timeout(foo.bar, 2)

    time.sleep(2.2)
    assert spy.call_count == 1

    time.sleep(2.2)
    assert spy.call_count == 1

    clear_timeout(i)


def test_clear_before_start(mocker):
    foo = Foo()
    spy = mocker.spy(foo, "bar")

    i = set_timeout(foo.bar, 10)

    start = time.time()

    time.sleep(2.2)

    clear_timeout(i)

    end = time.time()

    assert spy.call_count == 0

    assert end - start < 3


def test_set_multiple(mocker):
    foo = Foo()
    spy = mocker.spy(foo, "bar")

    i = set_interval(foo.bar, 2)
    j = set_timeout(foo.bar, 2)
    k = set_interval(foo.bar, 1)

    time.sleep(2.2)
    assert spy.call_count == 4

    time.sleep(2.2)
    assert spy.call_count == 7

    clear_interval(i)
    clear_timeout(j)
    clear_interval(k)

    time.sleep(2.2)
    assert spy.call_count == 7


def test_set_async_function(mocker):
    foo = Foo()
    spy = mocker.spy(foo, "async_bar")

    i = set_timeout(foo.async_bar, 2)

    time.sleep(2.2)
    assert spy.call_count == 1

    clear_timeout(i)
