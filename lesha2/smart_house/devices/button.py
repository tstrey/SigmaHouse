# -*- coding: utf-8 -*-
"""Provides Button device class."""

from time import ticks_diff, ticks_ms

from devices.device import Device

from machine import Pin

from micropython import schedule


class Button(Device):
    """Implements Button class."""

    def __init__(self, name="/in/button", pin_num=0, event_queue=None, debug=False):
        """Initiate object's internal state."""
        super().__init__(name=name, event_queue=event_queue, debug=debug)

        self._state = {
            "pressed": False,
            "pressed_for_ms": 0,
            "pressed_timestamp": 0,
            "released_timestamp": 0,
        }

        self._log(f"Initiating on pin {pin_num}")
        self._pin = Pin(pin_num, Pin.IN, Pin.PULL_UP)

        self._log("Registering IRQ")
        self._pin.irq(
            trigger=Pin.IRQ_RISING | Pin.IRQ_FALLING, handler=self._pin_callback
        )

    def _pin_callback(self, pin):
        """Synchronize button state with real world and message event queue."""
        if pin.value() == 0:
            self._state["pressed"] = True

            self._state["pressed_timestamp"] = ticks_ms()

            self._state["pressed_for_ms"] = 0
            self._state["released_timestamp"] = 0
        else:
            self._state["pressed"] = False

            self._state["released_timestamp"] = ticks_ms()

            self._state["pressed_for_ms"] = ticks_diff(
                self._state["released_timestamp"], self._state["pressed_timestamp"]
            )

        schedule(Button._push_event_state, self)

    def finalize(self):
        """De-register IRQ."""
        self._log("De-registering IRQ")
        self._pin.irq(handler=None)
