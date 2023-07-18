# -*- coding: utf-8 -*-
"""Stand-alone module with naive round robin scheduling."""

from time import sleep_ms, ticks_diff, ticks_ms

time_start = ticks_ms()

while True:
    # calculate uptime in seconds
    uptime_sec = ticks_diff(ticks_ms(), time_start) // 1000

    print(f"UPTIME[{uptime_sec:0>4}s]:")

    # wait for 5s
    sleep_ms(5000)
