"""
execution.py

Simulated execution handler.

Converts OrderEvents into FillEvents.
"""

from __future__ import annotations

from quantcore.events import (
    EventQueue,
    EventType,
    OrderEvent,
    FillEvent,
)
from quantcore.data import HistoricDataHandler


class SimulatedExecutionHandler:
    """
    Simulates a broker.

    Assumptions
    -----------
    - Instant market execution
    - Fixed commission
    - Percentage slippage
    """

    def __init__(
        self,
        events: EventQueue,
        data_handler: HistoricDataHandler,
        commission: float = 1.0,
        slippage: float = 0.001,
    ) -> None:

        self.events = events
        self.data_handler = data_handler

        self.commission = commission
        self.slippage = slippage

    # -----------------------------------------------------

    def execute_order(
        self,
        event: OrderEvent,
    ) -> None:

        if event.type != EventType.ORDER:
            return

        market_price = self.data_handler.get_latest_close()

        if event.action == "BUY":

            execution_price = (
                market_price
                * (1 + self.slippage)
            )

        else:

            execution_price = (
                market_price
                * (1 - self.slippage)
            )

        fill = FillEvent(
            symbol=event.symbol,
            timestamp=event.timestamp,
            action=event.action,
            quantity=event.quantity,
            price=execution_price,
            commission=self.commission,
        )

        self.events.put(fill)