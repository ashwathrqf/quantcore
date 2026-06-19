"""
event.py

Defines all events used by QuantCore.
"""

from __future__ import annotations

from abc import ABC
from dataclasses import dataclass
from datetime import datetime
from enum import Enum, auto


class EventType(Enum):

    MARKET = auto()

    SIGNAL = auto()

    ORDER = auto()

    FILL = auto()


class Event(ABC):

    @property
    def type(self):

        raise NotImplementedError


# =========================================================


@dataclass(slots=True)
class MarketEvent(Event):

    symbol: str

    timestamp: datetime

    @property
    def type(self):

        return EventType.MARKET


# =========================================================


@dataclass(slots=True)
class SignalEvent(Event):

    symbol: str

    timestamp: datetime

    action: str

    strength: float = 1.0

    @property
    def type(self):

        return EventType.SIGNAL


# =========================================================


@dataclass(slots=True)
class OrderEvent(Event):

    symbol: str

    timestamp: datetime

    action: str

    quantity: int

    @property
    def type(self):

        return EventType.ORDER


# =========================================================


@dataclass(slots=True)
class FillEvent(Event):

    symbol: str

    timestamp: datetime

    action: str

    quantity: int

    price: float

    commission: float

    @property
    def type(self):

        return EventType.FILL