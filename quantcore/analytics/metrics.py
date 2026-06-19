"""
metrics.py

Performance metrics for QuantCore.
"""

from __future__ import annotations

import numpy as np
import pandas as pd


class PerformanceMetrics:

    @staticmethod
    def returns(equity_curve):

        equity = pd.Series(equity_curve)

        return equity.pct_change().dropna()

    # --------------------------------------------------------

    @staticmethod
    def total_return(equity_curve):

        if len(equity_curve) < 2:
            return 0.0

        return (
            equity_curve[-1]
            - equity_curve[0]
        ) / equity_curve[0]

    # --------------------------------------------------------

    @staticmethod
    def cagr(
        equity_curve,
        periods_per_year=252,
    ):

        if len(equity_curve) < 2:
            return 0.0

        years = len(equity_curve) / periods_per_year

        return (
            equity_curve[-1]
            / equity_curve[0]
        ) ** (1 / years) - 1

    # --------------------------------------------------------

    @staticmethod
    def sharpe_ratio(
        equity_curve,
        risk_free_rate=0,
        periods_per_year=252,
    ):

        r = PerformanceMetrics.returns(
            equity_curve
        )

        if len(r) == 0:
            return 0.0

        std = r.std()

        if std == 0:
            return 0.0

        excess = (
            r
            - risk_free_rate / periods_per_year
        )

        return (
            np.sqrt(periods_per_year)
            * excess.mean()
            / std
        )

    # --------------------------------------------------------

    @staticmethod
    def max_drawdown(equity_curve):

        equity = pd.Series(equity_curve)

        running_max = equity.cummax()

        drawdown = (
            equity
            - running_max
        ) / running_max

        return abs(drawdown.min())