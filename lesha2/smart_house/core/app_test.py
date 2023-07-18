# -*- coding: utf-8 -*-
"""Provides main application object."""
from binascii import hexlify
from collections import deque
from time import ticks_ms


from devices.buzzer import Buzzer
from devices.device import Device


from machine import Pin, SoftI2C, Timer, unique_id

from micropython import schedule

from uasyncio import get_event_loop, sleep_ms

from ujson import dumps as json_dumps

from urequests import get as get_url, post as post_url, put as put_url


class App(Device):
    """Implements Smart House."""

    def __init__(self, name="/app_test", config=None, debug=False):
        """Initiate application."""
        super().__init__(name=name, debug=debug)

        self.event_queue = deque((), 10)
        self.unique_id = hexlify(unique_id()).decode("utf-8").upper()

        self._log(f"Running on board ID: {self.unique_id}")

        self.exit_code = 0


        self.buzzer = Buzzer(
            pin_num=26,
            event_queue=self.event_queue,
            debug=self._DEBUG,
        )
        
        self._buzzer_turn_on() 

    def __enter__(self):
        """Return class instance."""
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        """Gracefully exit by disconnecting from network and resetting I/O devices."""
        self._log("Exiting")


    def run(self):


        self._log("Exit event loop")
