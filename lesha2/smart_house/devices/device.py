# -*- coding: utf-8 -*-
"""Provides abstract device class."""

from time import time


class Device:
    """Implements Device class."""

    def __init__(self, name="/dev/null", event_queue=None, debug=False):
        """Initiate object's internal state."""
        self._DEBUG = debug
        self._name = name
        self._event_queue = event_queue
        self._state = {}

    def _push_event_state(self):
        """Push state to event queue."""
        event_data = {"source": self._name, "state": self._state}
        self._event_queue.append(event_data)

    def _log(self, msg):
        """Print debug log to serial console."""
        if self._DEBUG:
            print(f"UPTIME[{time():0>4}s]:/log{self._name}: {msg}")
