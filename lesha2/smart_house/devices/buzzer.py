# -*- coding: utf-8 -*-
"""Provides LED device class."""

from time import ticks_ms, sleep

from devices.device import Device

from machine import Pin, PWM


class Buzzer(Device):
    """Implements Buzz class."""

    def __init__(self, name="/out/buzzer", pin_num=0, event_queue=None, debug=False):
        """Initiate object's internal state."""
        super().__init__(name=name, event_queue=event_queue, debug=debug)

        self._state = {
            "active": False,
            "timestamp": 0,
        }

        self._log(f"Initiating on pin {pin_num}")
        self._log(f"about to start pin {pin_num}")
     #   self._pin = Pin(pin_num, Pin.OUT, value=0)
        self._buzzer = PWM(Pin(pin_num))
        self._buzzer.duty(0)
        self._log(f"set duty 0")
        self._buzzer.deinit()
        self._log("after deinit")

    def _set_buzzer(self):
        """Synchronize Buzzer  state with real world and message event queue."""
        self._log("in _set_buzzer")
        self._state["timestamp"] = ticks_ms()

   #     self._pin.value(self._state["active"])

        self._push_event_state()
        
    def turn_on(self):
        self._log(" IN BUZZER new!!")
        buzzer = PWM(Pin(26))

        buzzer.duty(1000) 

        # Happy birthday
        buzzer.freq(294)
        sleep(0.25)
        buzzer.freq(440)
        sleep(0.25)
        buzzer.freq(392)
        sleep(0.25)
        buzzer.freq(532)
        sleep(0.25)
        buzzer.freq(494)
        sleep(0.25)
        buzzer.freq(392)
        sleep(0.25)
        buzzer.freq(440)
        sleep(0.25)
        buzzer.freq(392)
        sleep(0.25)
        buzzer.freq(587)
        sleep(0.25)
        buzzer.freq(532)
        sleep(0.25)
        buzzer.freq(392)
        sleep(0.25)
        buzzer.freq(784)
        sleep(0.25)
        buzzer.freq(659)
        sleep(0.25)
        buzzer.freq(532)
        sleep(0.25)
        buzzer.freq(494)
        sleep(0.25)
        buzzer.freq(440)
        sleep(0.25)
        buzzer.freq(698)
        sleep(0.25)
        buzzer.freq(659)
        sleep(0.25)
        buzzer.freq(532)
        sleep(0.25)
        buzzer.freq(587)
        sleep(0.25)
        buzzer.freq(532)
        sleep(0.5)
        buzzer.duty(0)

    def turn_on_org(self):
        """Turn Buzzer on."""
        self._log(" IN BUZZER!!")
        self._log(self._state)
        if not self._state["active"]:
            self._log(" activating buzzer!!")
            self._state["active"] = True
            self._buzzer.duty(1000)
            self._buzzer.freq(294)
            self._log(" activating buzzer 1 !!")
            sleep(0.25)
            self._log(" activating buzzer 2 !!")
            self._set_buzzer()
            self._log(" activating buzzer 3 !!")
        else:
            self._log("no active in buzzer state!!")
            self._log(" activating buzzer!!")
            self._state["active"] = True
            self._buzzer.duty(1000)
            self._buzzer.freq(294)
            sleep(0.25)
            self._buzzer.freq(440)
            sleep(0.25)
            self._buzzer.freq(392)
            sleep(0.25)
            self._buzzer.freq(532)
            sleep(0.25)
            self._buzzer.freq(494)
            sleep(0.25)
            self._buzzer.freq(392)
            sleep(0.25)
            self._buzzer.freq(440)
            sleep(0.25)
            self._buzzer.freq(392)
            sleep(0.25)
            self._buzzer.freq(587)
            sleep(0.25)
            self._buzzer.freq(532)
            sleep(0.25)
            buzzer.duty(0)

            self._log(" activating buzzer 11 !!")
            self._log(" activating buzzer 21 !!")
            self._set_buzzer()
            self._log(" activating buzzer 31 !!")

    def turn_off(self):
        """Turn Buzzer off."""
        self._log("in turn_off")
        self._buzzer.deinit()
        if self._state["active"]:
            self._state["active"] = False


