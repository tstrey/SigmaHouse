# -*- coding: utf-8 -*-
"""Stand-alone module with dedicated LED state and button IRQ."""

from time import sleep_ms

from machine import Pin


def button1_callback(pin):
    """Print message."""
    print("!", end="")

    led_state["active"] = not led_state["active"]

    pin_set(led_state["pin"], led_state["active"])


def pin_set(pin, val):
    """Set output pin value."""
    if pin.value() != val:
        pin.value(val)


led_state = {"active": False, "pin": Pin(12, Pin.OUT, value=0)}

button1 = Pin(26, Pin.IN, Pin.PULL_UP)

button1.irq(trigger=Pin.IRQ_FALLING, handler=button1_callback)

while True:
    print(".", end="")

    # wait for 5s
    sleep_ms(5000)
