"""
strategy.py

Abstract base class for all trading strategies.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from queue import Queue

from quantcore.data import HistoricDataHandler
from quantcore.events import SignalEvent


class Strategy(ABC):
    """
    Abstract base strategy.

    Every strategy receives market data from the DataHandler
    and publishes SignalEvents to the event queue.
    """

    def __init__(
        self,
        events: Queue,
        data_handler: HistoricDataHandler,
    ) -> None:

        self.events = events
        self.data_handler = data_handler

    @abstractmethod
    def calculate_signals(self, event) -> None:
        """
        Generate trading signals from incoming MarketEvents.
        """
        raise NotImplementedError

    def buy(
        self,
        symbol: str,
        timestamp,
        strength: float = 1.0,
    ) -> None:
        """
        Generate a BUY signal.
        """

        signal = SignalEvent(
            symbol=symbol,
            timestamp=timestamp,
            action="BUY",
            strength=strength,
        )

        self.events.put(signal)

    def sell(
        self,
        symbol: str,
        timestamp,
        strength: float = 1.0,
    ) -> None:
        """
        Generate a SELL signal.
        """

        signal = SignalEvent(
            symbol=symbol,
            timestamp=timestamp,
            action="SELL",
            strength=strength,
        )

        self.events.put(signal)