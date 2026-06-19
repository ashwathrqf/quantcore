"""
engine.py

Core event-driven backtesting engine.
"""

from __future__ import annotations

from quantcore.events import (
    EventQueue,
    EventType,
)

from quantcore.data import HistoricDataHandler
from quantcore.strategy import SMACrossoverStrategy
from quantcore.portfolio import Portfolio
from quantcore.execution import SimulatedExecutionHandler


class BacktestEngine:

    def __init__(
        self,
        symbol: str,
        start: str,
        end: str,
        initial_capital: float = 100000,
        short_window=20,
        long_window=50,
        commission=1.0,
        slippage=0.001,
    ) -> None:

        self.events = EventQueue()

        self.data_handler = HistoricDataHandler(
            self.events,
            symbol,
            start,
            end,
        )

        self.strategy = SMACrossoverStrategy(
            self.events,
            self.data_handler,
            short_window,
            long_window,
        )

        self.portfolio = Portfolio(
            self.events,
            initial_capital,
        )

        self.execution = SimulatedExecutionHandler(
            self.events,
            self.data_handler,
            commission,
            slippage,
        )

    # --------------------------------------------------------

    def run(self):

        while self.data_handler.continue_backtest:

            # Load next market bar
            self.data_handler.update_bars()

            while not self.events.empty():

                event = self.events.get()

                if event is None:
                    continue

                # ---------------------------------------------

                if event.type == EventType.MARKET:

                    self.strategy.calculate_signals(
                        event
                    )

                    self.portfolio.update_market_value(
                        event.symbol,
                        self.data_handler.get_latest_close(),
                    )

                # ---------------------------------------------

                elif event.type == EventType.SIGNAL:

                    self.portfolio.update_signal(
                        event
                    )

                # ---------------------------------------------

                elif event.type == EventType.ORDER:

                    self.execution.execute_order(
                        event
                    )

                # ---------------------------------------------

                elif event.type == EventType.FILL:

                    self.portfolio.update_fill(
                        event
                    )

            # Record equity after all events for this bar
            self.portfolio.update_equity_curve()

        return self.results()

    # --------------------------------------------------------

    def results(self):

        return {

            "equity_curve":
                self.portfolio.equity_curve,

            "trade_history":
                self.portfolio.trade_history,

            "cash":
                self.portfolio.cash,

            "positions":
                self.portfolio.positions,

            "final_equity":
                self.portfolio.equity,

            "price_data":
                self.data_handler.data.copy()

        }