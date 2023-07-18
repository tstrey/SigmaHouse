# -*- coding: utf-8 -*-
"""Stand-alone module with naive button press detection (2 buttons)."""

from time import sleep_ms

from machine import Pin

button1 = Pin(26, Pin.IN, Pin.PULL_UP)
button2 = Pin(25, Pin.IN, Pin.PULL_UP)

while True:
    # Read value of PINs with buttons
    value_button1 = button1.value()
    value_button2 = button2.value()

    # Print those out in the shell
    if value_button1 == 1 and value_button2 == 1:
        print(".", end="")
    elif value_button1 == 0 and value_button2 == 1:
        print("1", end="")
    elif value_button1 == 1 and value_button2 == 0:
        print("2", end="")
    elif value_button1 == 0 and value_button2 == 0:
        print("!", end="")

    # wait 0.1s
    sleep_ms(100)
    # wait 1s
    # sleep_ms(1000)
    # wait 5s
    # sleep_ms(5000)
