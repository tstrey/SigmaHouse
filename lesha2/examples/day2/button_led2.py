# -*- coding: utf-8 -*-
"""Stand-alone module with setting LED based on single button input."""

from time import sleep_ms

from machine import Pin

button1 = Pin(26, Pin.IN, Pin.PULL_UP)

led_pin = Pin(12, Pin.OUT, value=0)


def pin_set(pin, val):
    """Set output pin value."""
    if pin.value() != val:
        pin.value(val)


while True:
    # Read value of PIN with button
    value_button1 = button1.value()

    # Print it out in the shell
    if value_button1 == 1:
        print(".", end="")
    else:
        print("!", end="")

    # Set LED pin output state based on inverted button input state
    pin_set(led_pin, not value_button1)

    # wait 0.1s
    sleep_ms(100)
