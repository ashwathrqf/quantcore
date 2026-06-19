"""
sma.py

Simple Moving Average crossover strategy.
"""

from __future__ import annotations

import pandas as pd

from quantcore.events import EventType
from quantcore.strategy.base import Strategy


class SMACrossoverStrategy(Strategy):

    def __init__(
        self,
        events,
        data_handler,
        short_window: int = 20,
        long_window: int = 50,
    ) -> None:

        super().__init__(events, data_handler)

        self.short_window = short_window
        self.long_window = long_window

        self.in_market = False

    # -----------------------------------------------------

    def calculate_signals(
        self,
        event,
    ) -> None:

        if event.type != EventType.MARKET:
            return

        bars = self.data_handler.get_latest_bars(
            self.long_window + 1
        )

        if len(bars) < self.long_window + 1:
            return

        close = bars["Close"]

        short_sma = (
            close
            .rolling(self.short_window)
            .mean()
        )

        long_sma = (
            close
            .rolling(self.long_window)
            .mean()
        )

        prev_short = short_sma.iloc[-2]
        prev_long = long_sma.iloc[-2]

        curr_short = short_sma.iloc[-1]
        curr_long = long_sma.iloc[-1]

        # ---------------- BUY ----------------

        if (
            prev_short <= prev_long
            and curr_short > curr_long
            and not self.in_market
        ):

            self.buy()

            self.in_market = True

        # ---------------- SELL ----------------

        elif (
            prev_short >= prev_long
            and curr_short < curr_long
            and self.in_market
        ):

            self.sell()

            self.in_market = False