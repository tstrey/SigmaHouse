# -*- coding: utf-8 -*-
"""Provides LED device class."""

from time import ticks_ms

from devices.device import Device

from machine import Pin


class LED(Device):
    """Implements LED class."""

    def __init__(self, name="/out/led", pin_num=0, event_queue=None, debug=False):
        """Initiate object's internal state."""
        super().__init__(name=name, event_queue=event_queue, debug=debug)

        self._state = {
            "active": False,
            "timestamp": 0,
        }

        self._log(f"Initiating on pin {pin_num}")
        self._pin = Pin(pin_num, Pin.OUT, value=0)

    def _set_led(self):
        """Synchronize LED state with real world and message event queue."""
        self._state["timestamp"] = ticks_ms()

        self._pin.value(self._state["active"])

        self._push_event_state()

    def turn_on(self):
        """Turn LED on."""
        if not self._state["active"]:
            self._state["active"] = True
            self._set_led()

    def turn_off(self):
        """Turn LED off."""
        if self._state["active"]:
            self._state["active"] = False
            self._set_led()

    def toggle(self):
        self._log(self._state)
        """if  LED off -> turn on, if on - turn off"""
        if self._state["active"]:
            self.turn_off()
        else:
            self.turn_on()