# -*- coding: utf-8 -*-
"""Stand-alone module with button press detection using IRQs."""

from time import sleep_ms

from machine import Pin


def button1_callback(pin):
    """Print button1 message."""
    print("1", end="")


def button2_callback(pin):
    """Print button2 message."""
    print("2", end="")


button1 = Pin(26, Pin.IN, Pin.PULL_UP)
button2 = Pin(25, Pin.IN, Pin.PULL_UP)

button1.irq(trigger=Pin.IRQ_FALLING, handler=button1_callback)
button2.irq(trigger=Pin.IRQ_FALLING, handler=button2_callback)

while True:
    print(".", end="")

    # wait for 5s
    sleep_ms(5000)
