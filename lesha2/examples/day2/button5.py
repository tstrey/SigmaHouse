# -*- coding: utf-8 -*-
"""Stand-alone module with button press detection using IRQs."""

from time import sleep_ms, ticks_diff, ticks_ms

from machine import Pin

button1_state = {
    "pressed": False,
    "pressed_for_ms": 0,
    "pressed_timestamp": 0,
    "released_timestamp": 0,
}

button2_state = {
    "pressed": False,
    "pressed_for_ms": 0,
    "pressed_timestamp": 0,
    "released_timestamp": 0,
}


def button1_callback(pin):
    """Change button1 state."""
    if pin.value() == 0:
        button1_state["pressed"] = True
        button1_state["pressed_timestamp"] = ticks_ms()

        button1_state["pressed_for_ms"] = 0
        button1_state["released_timestamp"] = 0
    else:
        button1_state["pressed"] = False
        button1_state["released_timestamp"] = ticks_ms()

        button1_state["pressed_for_ms"] = ticks_diff(
            button1_state["released_timestamp"], button1_state["pressed_timestamp"]
        )


def button2_callback(pin):
    """Change button2 state."""
    if pin.value() == 0:
        button2_state["pressed"] = True

        button2_state["pressed_timestamp"] = ticks_ms()

        button2_state["pressed_for_ms"] = 0
        button2_state["released_timestamp"] = 0
    else:
        button2_state["pressed"] = False

        button2_state["released_timestamp"] = ticks_ms()

        button2_state["pressed_for_ms"] = ticks_diff(
            button2_state["released_timestamp"], button2_state["pressed_timestamp"]
        )


button1 = Pin(26, Pin.IN, Pin.PULL_UP)
button2 = Pin(25, Pin.IN, Pin.PULL_UP)

button1.irq(trigger=Pin.IRQ_RISING | Pin.IRQ_FALLING, handler=button1_callback)
button2.irq(trigger=Pin.IRQ_RISING | Pin.IRQ_FALLING, handler=button2_callback)

time_start = ticks_ms()

try:
    while True:
        # calculate uptime in seconds
        uptime_sec = ticks_diff(ticks_ms(), time_start) // 1000

        print(f"UPTIME[{uptime_sec:0>4}s]: BUTTON1: {button1_state}")
        print(f"UPTIME[{uptime_sec:0>4}s]: BUTTON2: {button2_state}")

        # wait for 0.1s
        sleep_ms(100)
finally:
    button1.irq(handler=None)
    button2.irq(handler=None)
