# -*- coding: utf-8 -*-
"""Stand-alone module with single button press detection."""

from time import sleep_ms

from machine import Pin

button1 = Pin(26, Pin.IN, Pin.PULL_UP)

while True:
    # Read value of PIN with button
    value_button1 = button1.value()

    # Print it out in the shell
    if value_button1 == 1:
        print(".", end="")
    else:
        print("!", end="")

    # wait 0.1s
    sleep_ms(100)
