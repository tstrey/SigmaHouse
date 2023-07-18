# -*- coding: utf-8 -*-
"""Stand-alone module with button press detection using IRQs."""

from time import sleep_ms, ticks_diff, ticks_ms

from machine import Pin


class Button:
    """Implements Button class."""

    def __init__(self, pin_num):
        """Initiate object's internal state."""
        print("BUTTON: Initiating")

        self._pin = Pin(pin_num, Pin.IN, Pin.PULL_UP)

        self._state = {
            "pressed": False,
            "pressed_for_ms": 0,
            "pressed_timestamp": 0,
            "released_timestamp": 0,
        }

        print(f"BUTTON: Registering IRQ for pin: {self._pin}")
        self._pin.irq(
            trigger=Pin.IRQ_RISING | Pin.IRQ_FALLING, handler=self._pin_callback
        )

    def _pin_callback(self, pin):
        """Synchronize button state with real world."""
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

    def get_state(self):
        """Return current state."""
        return self._state

    def finalize(self):
        """De-register IRQ."""
        print(f"BUTTON: De-registering IRQ for pin: {self._pin}")
        self._pin.irq(handler=None)


button1 = Button(26)
button2 = Button(25)

time_start = ticks_ms()

try:
    while True:
        # calculate uptime in seconds
        uptime_sec = ticks_diff(ticks_ms(), time_start) // 1000

        print(f"UPTIME[{uptime_sec:0>4}s]: BUTTON1: {button1.get_state()}")
        print(f"UPTIME[{uptime_sec:0>4}s]: BUTTON2: {button2.get_state()}")

        # wait for 0.1s
        sleep_ms(100)

except KeyboardInterrupt:
    print("Caught keyboard interrupt.")
    raise

finally:
    button1.finalize()
    button2.finalize()
