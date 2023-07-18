# -*- coding: utf-8 -*-
"""Provides TextMenu class."""
from time import time


class TextMenu:
    """Implements text menu class."""

    DEBUG = False

    def __init__(self, name="/menu", event_queue=None, debug=False):
        """Initiate object's internal state."""
        self._DEBUG = debug
        self._name = name
        self._event_queue = event_queue

        self._log("Initiating")

        self._menu_content = []
        self._menu_index = 0

    def _log(self, msg):
        """Print debug log to serial console."""
        if self._DEBUG:
            print(f"UPTIME[{time():0>4}s]:/log{self._name}: {msg}")

    def add_item(self, content, action=None):
        """Add item content and action."""
        self._menu_content.append({"content": content, "action": action})

        self._log(f"Add item: {content}")

    def move_next(self):
        """Move to next menu item."""
        self._menu_index += 1

        if self._menu_index == len(self._menu_content):
            self._menu_index = 0

        self._log(f"Moved to: {self.get_current_content()}")

    def get_current_content(self):
        """Get current menu item content."""
        content = self._menu_content[self._menu_index]["content"]

        return content

    def get_current_action(self):
        """Execute current menu item action."""
        action = self._menu_content[self._menu_index]["action"]

        return action
