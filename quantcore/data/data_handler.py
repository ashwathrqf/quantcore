"""
data_handler.py

Historical market data handler for QuantCore.
"""

from __future__ import annotations

import pandas as pd
import yfinance as yf

from quantcore.events import EventQueue, MarketEvent


class HistoricDataHandler:
    """
    Downloads and streams historical market data.
    """

    def __init__(
        self,
        events: EventQueue,
        symbol: str,
        start: str,
        end: str,
        interval: str = "1d",
    ) -> None:

        self.events = events

        self.symbol = symbol.upper()

        self.start = start

        self.end = end

        self.interval = interval

        self.current_bar = 0

        self.continue_backtest = True

        self.data = self._download_data()

    # -----------------------------------------------------

    def _download_data(self) -> pd.DataFrame:

        data = yf.download(
            self.symbol,
            start=self.start,
            end=self.end,
            interval=self.interval,
            auto_adjust=False,
            progress=False,
        )

        if data.empty:

            raise ValueError(
                f"No data found for '{self.symbol}'."
            )

        data.dropna(inplace=True)

        # Handle yfinance MultiIndex columns
        if isinstance(data.columns, pd.MultiIndex):
            data.columns = data.columns.get_level_values(0)

        return data

    # -----------------------------------------------------

    def update_bars(self) -> None:

        if self.current_bar >= len(self.data):

            self.continue_backtest = False

            return

        timestamp = self.data.index[self.current_bar]

        self.events.put(

            MarketEvent(

                symbol=self.symbol,

                timestamp=timestamp,

            )

        )

        self.current_bar += 1

    # -----------------------------------------------------

    def get_latest_bar(self):

        return self.data.iloc[self.current_bar - 1]

    # -----------------------------------------------------

    def get_latest_bars(
        self,
        n: int = 1,
    ):

        start = max(0, self.current_bar - n)

        return self.data.iloc[start:self.current_bar]

    # -----------------------------------------------------

    def get_latest_close(self) -> float:

        return float(

            self.get_latest_bar()["Close"]

        )

    # -----------------------------------------------------

    def get_current_time(self):

        return self.data.index[self.current_bar - 1]