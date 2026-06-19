"""
base.py

Abstract base class for all trading strategies.
"""

from __future__ import annotations

from abc import ABC, abstractmethod

from quantcore.data import HistoricDataHandler
from quantcore.events import (
    EventQueue,
    MarketEvent,
    SignalEvent,
)


class Strategy(ABC):
    """
    Base class for all trading strategies.
    """

    def __init__(
        self,
        events: EventQueue,
        data_handler: HistoricDataHandler,
    ) -> None:

        self.events = events
        self.data_handler = data_handler

    @abstractmethod
    def calculate_signals(
        self,
        event: MarketEvent,
    ) -> None:
        """
        Generate trading signals.
        """
        pass

    # -----------------------------------------------------

    def buy(
        self,
        strength: float = 1.0,
    ) -> None:

        signal = SignalEvent(
            symbol=self.data_handler.symbol,
            timestamp=self.data_handler.get_current_time(),
            action="BUY",
            strength=strength,
        )

        self.events.put(signal)

    # -----------------------------------------------------

    def sell(
        self,
        strength: float = 1.0,
    ) -> None:

        signal = SignalEvent(
            symbol=self.data_handler.symbol,
            timestamp=self.data_handler.get_current_time(),
            action="SELL",
            strength=strength,
        )

        self.events.put(signal)