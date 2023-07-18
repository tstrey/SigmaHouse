# -*- coding: utf-8 -*-
"""Stand-alone module blinking LED."""

from time import sleep_ms

from machine import Pin

led_pin = Pin(12, Pin.OUT, value=0)


def pin_toggle(pin):
    """Toggle pin output."""
    pin.value(not pin.value())


while True:
    pin_toggle(led_pin)

    # wait 0.1s
    sleep_ms(500)

    print(".", end="")
