import time

from microcontroller import watchdog
from watchdog import WatchDogMode

g_timeout_secs = 30

class WdHelper:

    @staticmethod
    def wd_init(timeout_secs = 30):
        global g_timeout_secs
        g_timeout_secs = timeout_secs
        watchdog.timeout = timeout_secs
        watchdog.mode = WatchDogMode.RESET

    @staticmethod
    def wd_sleep(sleep_time):
        global g_timeout_secs
        watchdog.feed()
        max_sleep_time = g_timeout_secs/2
        while sleep_time > 0:
            cur_sleep = sleep_time if sleep_time < max_sleep_time else max_sleep_time
            time.sleep(cur_sleep)
            sleep_time -= cur_sleep
            watchdog.feed()
