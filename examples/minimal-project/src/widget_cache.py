"""Illustrative widget cache for the Socratic Garden example project.

This file exists only to give the example project a `src/` source directory.
It is not part of Socratic Garden itself.
"""

from collections import OrderedDict


class WidgetCache:
    """A tiny least-recently-used cache, for demonstration purposes."""

    def __init__(self, max_items: int = 500) -> None:
        self.max_items = max_items
        self._items: "OrderedDict[str, object]" = OrderedDict()

    def get(self, key: str):
        if key not in self._items:
            return None
        self._items.move_to_end(key)
        return self._items[key]

    def put(self, key: str, value: object) -> None:
        self._items[key] = value
        self._items.move_to_end(key)
        while len(self._items) > self.max_items:
            self._items.popitem(last=False)
