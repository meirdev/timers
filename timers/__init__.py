from .timers import Timers

_timers = Timers()

set_interval = _timers.set_interval
clear_interval = _timers.clear_interval

set_timeout = _timers.set_timeout
clear_timeout = _timers.clear_timeout
