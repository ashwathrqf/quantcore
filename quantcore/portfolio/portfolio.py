"""
portfolio.py

Portfolio management for QuantCore.

Responsibilities
----------------
- Convert SignalEvents into OrderEvents
- Track cash
- Track positions
- Process FillEvents
- Maintain portfolio equity
"""

from __future__ import annotations

from quantcore.events import (
    EventQueue,
    EventType,
    SignalEvent,
    OrderEvent,
    FillEvent,
)


class Portfolio:

    def __init__(
        self,
        events: EventQueue,
        initial_capital: float = 100000.0,
        position_size: int = 100,
    ) -> None:

        self.events = events

        self.initial_capital = initial_capital
        self.cash = initial_capital

        self.position_size = position_size

        # symbol -> shares held
        self.positions: dict[str, int] = {}

        # latest market prices
        self.latest_prices: dict[str, float] = {}

        # equity history
        self.equity_curve: list[float] = []

        # executed trades
        self.trade_history: list[FillEvent] = []

    # ---------------------------------------------------------

    def update_signal(
        self,
        event: SignalEvent,
    ) -> None:
        """
        Convert SignalEvent into OrderEvent.
        """

        if event.type != EventType.SIGNAL:
            return

        # Prevent selling without a position
        if (
            event.action == "SELL"
            and self.positions.get(event.symbol, 0) == 0
        ):
            return

        order = OrderEvent(
            symbol=event.symbol,
            timestamp=event.timestamp,
            action=event.action,
            quantity=self.position_size,
        )

        self.events.put(order)

        # ---------------------------------------------------------

    def update_fill(
        self,
        event: FillEvent,
    ) -> None:
        """
        Update portfolio after an executed trade.
        """

        if event.type != EventType.FILL:
            return

        symbol = event.symbol

        if symbol not in self.positions:
            self.positions[symbol] = 0

        trade_value = event.price * event.quantity

        if event.action == "BUY":

            self.positions[symbol] += event.quantity

            self.cash -= (
                trade_value + event.commission
            )

        elif event.action == "SELL":

            self.positions[symbol] -= event.quantity

            self.cash += (
                trade_value - event.commission
            )

        self.trade_history.append(event)

    # ---------------------------------------------------------

    # ---------------------------------------------------------

    def update_market_value(
        self,
        symbol: str,
        price: float,
    ) -> None:
        """
        Store the latest market price for a symbol.
        """

        self.latest_prices[symbol] = price


    # ---------------------------------------------------------

    def total_market_value(self) -> float:
        """
        Current market value of all holdings.
        """

        value = 0.0

        for symbol, quantity in self.positions.items():

            price = self.latest_prices.get(symbol, 0.0)

            value += quantity * price

        return value


    # ---------------------------------------------------------

    @property
    def equity(self) -> float:
        """
        Total portfolio equity.
        """

        return self.cash + self.total_market_value()


    # ---------------------------------------------------------

    def update_equity_curve(self) -> None:
        """
        Append current equity to the equity curve.
        """

        self.equity_curve.append(self.equity)