# -*- coding: utf-8 -*-
"""Provides LED device class."""

from time import ticks_ms

from devices.device import Device

from machine import Pin

from micropython import schedule


class Motion(Device):
    """Implements Motion class."""

    def __init__(self, name="/in/motion", pin_num=0, event_queue=None, debug=False):
        """Initiate object's internal state."""
        super().__init__(name=name, event_queue=event_queue, debug=debug)

        self._state = {
            "motion_alarm": False,
        }

        self._log(f"Initiating on pin {pin_num}")
        self._pin = Pin(pin_num, Pin.IN)

        self._log("Registering IRQ")
        self._pin.irq(
            trigger=Pin.IRQ_RISING | Pin.IRQ_FALLING, handler=self._pin_callback
        )

    def _pin_callback(self, pin):
        """Synchronize motion state with real world and message event queue."""
        if pin.value() == 1:
            self._state["motion_alarm"] = True
        else:
            self._state["motion_alarm"] = False

        schedule(Motion._push_event_state, self)

    def finalize(self):
        """De-register IRQ."""
        self._log("De-registering IRQ")
        self._pin.irq(handler=None)

