# Timers

`set_interval` and `set_timeout` for Python.

## Example

### set_interval

```python
import time
from timers import set_interval, clear_interval

def print_hello():
    print("hello")

interval = set_interval(print_hello, 1)  # prints "hello" every second

time.sleep(5)

clear_interval(interval)  # stops the interval
```

### set_timeout

```python
from timers import set_timeout, clear_timeout

def print_hello():
    print("hello")

timeout = set_timeout(print_hello, 1)  # prints "hello" after one second

clear_timeout(timeout)
```
