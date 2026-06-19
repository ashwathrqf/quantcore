import streamlit as st
import pandas as pd
from dataclasses import asdict
import plotly.graph_objects as go

from quantcore.engine import BacktestEngine
from quantcore.analytics import PerformanceMetrics

st.set_page_config(
    page_title="QuantCore",
    layout="wide",
)

st.title("📈 QuantCore Event-Driven Backtester")

# ----------------------------------------------------

st.sidebar.header("⚙️ Backtest Configuration")

symbol = st.sidebar.text_input(
    "Ticker",
    value="AAPL",
)

start = st.sidebar.date_input(
    "Start Date",
    pd.Timestamp("2022-01-01"),
)

end = st.sidebar.date_input(
    "End Date",
    pd.Timestamp.today(),
)

capital = st.sidebar.number_input(
    "Initial Capital ($)",
    value=100000,
    step=1000,
)

st.sidebar.divider()

st.sidebar.subheader("Strategy")

short_window = st.sidebar.slider(
    "Short SMA",
    min_value=5,
    max_value=50,
    value=20,
)

long_window = st.sidebar.slider(
    "Long SMA",
    min_value=20,
    max_value=200,
    value=50,
)

st.sidebar.divider()

st.sidebar.subheader("Execution")

commission = st.sidebar.number_input(
    "Commission ($)",
    value=1.0,
    step=0.5,
)

slippage = (
    st.sidebar.slider(
        "Slippage (%)",
        min_value=0.0,
        max_value=1.0,
        value=0.1,
        step=0.01,
    ) / 100
)

run = st.sidebar.button(
    "🚀 Run Backtest",
    use_container_width=True,
)

# ----------------------------------------------------

if run:

    engine = BacktestEngine(
        symbol,
        str(start),
        str(end),
        capital,
        short_window,
        long_window,
        commission,
        slippage,
    )

    results = engine.run()

    equity = results["equity_curve"]

    price_data = results["price_data"]

    trades = pd.DataFrame(
        [asdict(t) for t in results["trade_history"]]
    )

    st.subheader("Performance")

    c1, c2, c3, c4,c5 = st.columns(5)

    c1.metric(
        "Total Return",
        f"{PerformanceMetrics.total_return(equity):.2%}",
    )

    c2.metric(
        "Sharpe",
        f"{PerformanceMetrics.sharpe_ratio(equity):.2f}",
    )

    c3.metric(
        "Max Drawdown",
        f"{PerformanceMetrics.max_drawdown(equity):.2%}",
    )

    c4.metric(
        "Final Equity",
        f"${results['final_equity']:.2f}",
    )

    c5.metric(
    "Trades",
    len(results["trade_history"])
    )

    st.subheader("📈 Price Chart with Trade Signals")

    fig_price = go.Figure()

    fig_price.add_trace(
        go.Scatter(
            x=price_data.index,
            y=price_data["Close"],
            mode="lines",
            name="Close Price",
        )
    )

    if not trades.empty:

        buys = trades[trades["action"] == "BUY"]

        sells = trades[trades["action"] == "SELL"]

        fig_price.add_trace(
            go.Scatter(
                x=buys["timestamp"],
                y=buys["price"],
                mode="markers",
                marker=dict(
                    symbol="triangle-up",
                    size=11,
                    color="green",
                ),
                name="BUY",
            )
        )

        fig_price.add_trace(
            go.Scatter(
                x=sells["timestamp"],
                y=sells["price"],
                mode="markers",
                marker=dict(
                    symbol="triangle-down",
                    size=11,
                    color="red",
                ),
                name="SELL",
            )
        )

    fig_price.update_layout(
        height=500,
        xaxis_title="Date",
        yaxis_title="Price ($)",
    )

    st.plotly_chart(
        fig_price,
        use_container_width=True,
    )

    st.divider()



    st.subheader("📊 Portfolio Equity Curve")

    fig = go.Figure()

    fig.add_trace(
        go.Scatter(
            x=price_data.index[:len(equity)],
            y=equity,
            mode="lines",
            name="Portfolio Equity",
        )
    )

    fig.update_layout(
        title="Portfolio Equity Curve",
        xaxis_title="Date",
        yaxis_title="Portfolio Value ($)",
    )

    st.plotly_chart(
        fig,
        use_container_width=True,
    )

    st.subheader("Trades")

    if len(trades):

        st.dataframe(
            trades,
            use_container_width=True,
        )