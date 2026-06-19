"""
event_queue.py

Central event queue for QuantCore.
"""

from queue import Queue


class EventQueue(Queue):
    """
    Thin wrapper around Python's Queue.

    This abstraction allows the queue implementation
    to be replaced in the future without changing
    the rest of the framework.
    """

    pass