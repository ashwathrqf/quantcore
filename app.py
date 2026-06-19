import streamlit as st
import pandas as pd
from dataclasses import asdict
import plotly.graph_objects as go

from quantcore.engine import BacktestEngine
from quantcore.analytics import PerformanceMetrics

st.set_page_config(page_title="QuantCore", page_icon="🧮", layout="wide")

# ==========================================
# DESIGN SYSTEM — "research desk" theme
# Light, paper-and-ink dashboard with a navy/
# green/red signal palette grounded in the
# engine's own Market → Signal → Order → Fill
# event pipeline.
# ==========================================
def inject_theme():
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Sora:wght@500;600;700&family=Public+Sans:wght@400;500;600&family=IBM+Plex+Mono:wght@400;500;600&display=swap');

    :root {
        --bg-base: #EEF1F6;
        --bg-surface: #FFFFFF;
        --bg-surface-soft: #F5F8FB;
        --border: #DCE3EC;
        --ink: #121826;
        --ink-soft: #5B6678;
        --gain: #1F7A53;
        --loss: #B83A3A;
        --accent: #2A4D8F;
        --accent-soft: #E7EDF8;
    }

    html, body, .stApp { background: var(--bg-base); font-family: 'Public Sans', sans-serif; }
    .stApp { color: var(--ink); }
    #MainMenu, footer { visibility: hidden; }
    header[data-testid="stHeader"] { background: transparent; }
    .block-container { padding-top: 2rem; max-width: 1220px; }

    ::-webkit-scrollbar { width: 8px; height: 8px; }
    ::-webkit-scrollbar-thumb { background: var(--border); border-radius: 8px; }
    ::-webkit-scrollbar-track { background: transparent; }
    button:focus-visible, input:focus-visible { outline: 2px solid var(--accent); outline-offset: 2px; }

    /* ---- Hero ---- */
    .qc-eyebrow { font-family: 'IBM Plex Mono', monospace; font-size: 0.72rem; letter-spacing: 0.16em;
        text-transform: uppercase; color: var(--accent); margin-bottom: 0.5rem; }
    .qc-title { font-family: 'Sora', sans-serif; font-weight: 700; font-size: 2.3rem; color: var(--ink);
        margin: 0; line-height: 1.1; }
    .qc-subtitle { color: var(--ink-soft); font-size: 1rem; margin-top: 0.6rem; max-width: 640px; line-height: 1.55; }

    /* ---- Event pipeline signature ---- */
    .qc-pipeline { display: flex; align-items: center; margin: 1.5rem 0 2rem; }
    .qc-node { font-family: 'IBM Plex Mono', monospace; font-size: 0.66rem; letter-spacing: 0.08em;
        text-transform: uppercase; color: var(--ink); background: var(--bg-surface);
        border: 1px solid var(--border); padding: 0.4rem 0.75rem; border-radius: 7px; white-space: nowrap; }
    .qc-pipe { flex: 1; height: 2px; min-width: 24px; margin: 0 6px; border-radius: 2px;
        background: repeating-linear-gradient(90deg, var(--accent) 0 6px, transparent 6px 12px);
        background-size: 24px 100%; animation: qc-flow 1.4s linear infinite; }
    @keyframes qc-flow { from { background-position: 0 0; } to { background-position: -24px 0; } }

    /* ---- Sidebar ---- */
    section[data-testid="stSidebar"] { background: var(--bg-surface); border-right: 1px solid var(--border); }
    .qc-brand { display: flex; align-items: center; gap: 0.6rem; margin-bottom: 1.2rem; }
    .qc-brand-mark { font-family: 'Sora', sans-serif; font-weight: 700; font-size: 1.1rem; color: #fff;
        background: var(--accent); width: 32px; height: 32px; border-radius: 8px; display: flex;
        align-items: center; justify-content: center; }
    .qc-brand-title { font-family: 'Sora', sans-serif; font-weight: 700; font-size: 1rem; color: var(--ink); }
    .qc-brand-sub { font-family: 'IBM Plex Mono', monospace; font-size: 0.62rem; letter-spacing: 0.1em;
        color: var(--ink-soft); text-transform: uppercase; margin-top: 1px; }
    .qc-section-label { font-family: 'IBM Plex Mono', monospace; font-size: 0.66rem; letter-spacing: 0.13em;
        text-transform: uppercase; color: var(--ink-soft); margin: 1.4rem 0 0.6rem; padding-top: 1rem;
        border-top: 1px solid var(--border); }
    .qc-section-label:first-of-type { border-top: none; padding-top: 0; margin-top: 0.2rem; }

    /* ---- Cards ---- */
    .qc-card-header { font-family: 'Sora', sans-serif; font-weight: 600; font-size: 1rem; color: var(--ink);
        margin-bottom: 0.8rem; }
    .qc-section-divider { font-family: 'IBM Plex Mono', monospace; font-size: 0.7rem; letter-spacing: 0.12em;
        text-transform: uppercase; color: var(--ink-soft); margin: 2rem 0 0.8rem; padding-top: 1.2rem;
        border-top: 1px solid var(--border); }

    /* ---- KPI row ---- */
    .qc-kpi-row { display: flex; gap: 1rem; flex-wrap: wrap; animation: qc-fade-in 0.45s ease both; }
    @keyframes qc-fade-in { from { opacity: 0; transform: translateY(6px); } to { opacity: 1; transform: translateY(0); } }
    .qc-kpi { flex: 1; min-width: 170px; background: var(--bg-surface); border: 1px solid var(--border);
        border-top: 3px solid var(--accent); border-radius: 12px; padding: 1rem 1.2rem;
        box-shadow: 0 6px 16px rgba(18,24,38,0.05); }
    .qc-kpi-label { font-family: 'IBM Plex Mono', monospace; font-size: 0.65rem; letter-spacing: 0.1em;
        color: var(--ink-soft); text-transform: uppercase; margin-bottom: 0.45rem; }
    .qc-kpi-value { font-family: 'Sora', sans-serif; font-weight: 700; font-size: 1.5rem; }

    /* ---- Streamlit widget overrides ---- */
    div[data-testid="stButton"] button {
        background: var(--accent); color: #fff; font-family: 'Sora', sans-serif; font-weight: 600;
        border: none; border-radius: 9px; padding: 0.6rem 1.1rem;
        transition: transform 0.15s ease, box-shadow 0.15s ease;
    }
    div[data-testid="stButton"] button:hover { transform: translateY(-1px); box-shadow: 0 6px 16px rgba(42,77,143,0.3); }

    div[data-testid="stTextInput"] input, div[data-testid="stNumberInput"] input, div[data-testid="stDateInput"] input {
        background: var(--bg-surface-soft); border: 1px solid var(--border); color: var(--ink);
        font-family: 'IBM Plex Mono', monospace; border-radius: 8px;
    }
    div[data-testid="stTextInput"] input:focus, div[data-testid="stNumberInput"] input:focus,
    div[data-testid="stDateInput"] input:focus { border-color: var(--accent); box-shadow: 0 0 0 3px rgba(42,77,143,0.12); }

    div[data-testid="stSlider"] label p { color: var(--ink-soft) !important; font-size: 0.85rem; }
    div[data-testid="stSlider"] div[role="slider"] { background-color: var(--accent) !important; }
    div[data-testid="stSlider"] div[data-baseweb="slider"] > div > div { background: var(--accent) !important; }

    div[data-testid="stVerticalBlockBorderWrapper"] {
        background: var(--bg-surface) !important; border: 1px solid var(--border) !important;
        border-radius: 14px !important; box-shadow: 0 6px 18px rgba(18,24,38,0.05);
    }
    section[data-testid="stSidebar"] hr { border-color: var(--border); }

    div[data-testid="stDataFrame"] { border: 1px solid var(--border); border-radius: 12px; overflow: hidden; }

    @media (max-width: 768px) {
        .qc-title { font-size: 1.6rem; }
        .qc-kpi-row { flex-direction: column; }
    }
    </style>
    """, unsafe_allow_html=True)

inject_theme()

PLOT_FONT = dict(family="Public Sans, sans-serif", color="#121826", size=12)

def style_figure(fig):
    fig.update_layout(
        plot_bgcolor="#FFFFFF",
        paper_bgcolor="#FFFFFF",
        font=PLOT_FONT,
        margin=dict(l=10, r=10, t=10, b=10),
        hovermode="x unified",
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1,
                    bgcolor="rgba(0,0,0,0)"),
        xaxis=dict(gridcolor="#EEF1F6", showline=True, linecolor="#DCE3EC", title=fig.layout.xaxis.title),
        yaxis=dict(gridcolor="#EEF1F6", showline=True, linecolor="#DCE3EC", title=fig.layout.yaxis.title),
    )
    return fig

def render_hero():
    st.markdown("""
    <div class="qc-eyebrow">Event-Driven Backtesting Engine</div>
    <div class="qc-title">QuantCore</div>
    <div class="qc-subtitle">Configure a strategy, replay it bar-by-bar through a market → signal → order → fill
        event pipeline, and inspect the resulting performance.</div>
    <div class="qc-pipeline">
        <div class="qc-node">Market</div><div class="qc-pipe"></div>
        <div class="qc-node">Signal</div><div class="qc-pipe"></div>
        <div class="qc-node">Order</div><div class="qc-pipe"></div>
        <div class="qc-node">Fill</div>
    </div>
    """, unsafe_allow_html=True)

def render_kpis(total_return, sharpe, max_dd, final_equity, capital, trades_count):
    return_color = "var(--gain)" if total_return >= 0 else "var(--loss)"
    sharpe_color = "var(--gain)" if sharpe >= 1 else ("var(--loss)" if sharpe < 0 else "var(--ink-soft)")
    equity_color = "var(--gain)" if final_equity >= capital else "var(--loss)"
    st.markdown(f"""
    <div class="qc-kpi-row">
        <div class="qc-kpi" style="border-top-color: {return_color};">
            <div class="qc-kpi-label">Total Return</div>
            <div class="qc-kpi-value" style="color: {return_color};">{total_return:.2%}</div>
        </div>
        <div class="qc-kpi" style="border-top-color: {sharpe_color};">
            <div class="qc-kpi-label">Sharpe Ratio</div>
            <div class="qc-kpi-value" style="color: {sharpe_color};">{sharpe:.2f}</div>
        </div>
        <div class="qc-kpi" style="border-top-color: var(--loss);">
            <div class="qc-kpi-label">Max Drawdown</div>
            <div class="qc-kpi-value" style="color: var(--loss);">{max_dd:.2%}</div>
        </div>
        <div class="qc-kpi" style="border-top-color: {equity_color};">
            <div class="qc-kpi-label">Final Equity</div>
            <div class="qc-kpi-value" style="color: {equity_color};">${final_equity:,.2f}</div>
        </div>
        <div class="qc-kpi" style="border-top-color: var(--accent);">
            <div class="qc-kpi-label">Trades</div>
            <div class="qc-kpi-value" style="color: var(--ink);">{trades_count}</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

render_hero()

# ----------------------------------------------------
# SIDEBAR — CONFIGURATION
# ----------------------------------------------------
with st.sidebar:
    st.markdown("""
    <div class="qc-brand">
        <div class="qc-brand-mark">Q</div>
        <div>
            <div class="qc-brand-title">QuantCore</div>
            <div class="qc-brand-sub">Backtest Configuration</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="qc-section-label">Universe &amp; Capital</div>', unsafe_allow_html=True)
    symbol = st.text_input("Ticker", value="AAPL")
    start = st.date_input("Start Date", pd.Timestamp("2022-01-01"))
    end = st.date_input("End Date", pd.Timestamp.today())
    capital = st.number_input("Initial Capital ($)", value=100000, step=1000)

    st.markdown('<div class="qc-section-label">Strategy · SMA Crossover</div>', unsafe_allow_html=True)
    short_window = st.slider("Short SMA", min_value=5, max_value=50, value=20)
    long_window = st.slider("Long SMA", min_value=20, max_value=200, value=50)

    st.markdown('<div class="qc-section-label">Execution</div>', unsafe_allow_html=True)
    commission = st.number_input("Commission ($)", value=1.0, step=0.5)
    slippage = st.slider("Slippage (%)", min_value=0.0, max_value=1.0, value=0.1, step=0.01) / 100

    st.markdown("<div style='height: 0.6rem;'></div>", unsafe_allow_html=True)
    run = st.button("Run Backtest", use_container_width=True)

# ----------------------------------------------------
# MAIN — RESULTS
# ----------------------------------------------------
if run:

    # NOTE: this calls BacktestEngine with the 8-arg signature this UI was built
    # against (symbol, start, end, capital, short_window, long_window, commission,
    # slippage). The engine.py currently on disk only accepts 4 args
    # (symbol, start, end, initial_capital) and results() doesn't return
    # "price_data" — wire those through on the engine side for this to run.
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
    trades = pd.DataFrame([asdict(t) for t in results["trade_history"]])

    total_return = PerformanceMetrics.total_return(equity)
    sharpe = PerformanceMetrics.sharpe_ratio(equity)
    max_dd = PerformanceMetrics.max_drawdown(equity)

    st.markdown('<div class="qc-section-divider">Performance</div>', unsafe_allow_html=True)
    render_kpis(total_return, sharpe, max_dd, results["final_equity"], capital, len(results["trade_history"]))

    st.markdown('<div class="qc-section-divider">Price Action &amp; Trade Signals</div>', unsafe_allow_html=True)
    with st.container(border=True):
        fig_price = go.Figure()

        fig_price.add_trace(go.Scatter(
            x=price_data.index, y=price_data["Close"], mode="lines", name="Close Price",
            line=dict(color="#2A4D8F", width=2),
            hovertemplate="%{x|%b %d, %Y}<br>$%{y:,.2f}<extra></extra>",
        ))

        if not trades.empty:
            buys = trades[trades["action"] == "BUY"]
            sells = trades[trades["action"] == "SELL"]

            fig_price.add_trace(go.Scatter(
                x=buys["timestamp"], y=buys["price"], mode="markers",
                marker=dict(symbol="triangle-up", size=11, color="#1F7A53", line=dict(width=1, color="#FFFFFF")),
                name="BUY", hovertemplate="%{x|%b %d, %Y}<br>Buy @ $%{y:,.2f}<extra></extra>",
            ))

            fig_price.add_trace(go.Scatter(
                x=sells["timestamp"], y=sells["price"], mode="markers",
                marker=dict(symbol="triangle-down", size=11, color="#B83A3A", line=dict(width=1, color="#FFFFFF")),
                name="SELL", hovertemplate="%{x|%b %d, %Y}<br>Sell @ $%{y:,.2f}<extra></extra>",
            ))

        fig_price.update_layout(height=460, xaxis_title="Date", yaxis_title="Price ($)")
        st.plotly_chart(style_figure(fig_price), use_container_width=True)

    st.markdown('<div class="qc-section-divider">Portfolio Equity Curve</div>', unsafe_allow_html=True)
    with st.container(border=True):
        fig_equity = go.Figure()

        fig_equity.add_trace(go.Scatter(
            x=price_data.index[:len(equity)], y=equity, mode="lines", name="Portfolio Equity",
            line=dict(color="#0F766E", width=2),
            hovertemplate="%{x|%b %d, %Y}<br>$%{y:,.2f}<extra></extra>",
        ))

        fig_equity.update_layout(height=420, xaxis_title="Date", yaxis_title="Portfolio Value ($)")
        st.plotly_chart(style_figure(fig_equity), use_container_width=True)

    st.markdown('<div class="qc-section-divider">Trade Log</div>', unsafe_allow_html=True)
    if len(trades):
        with st.container(border=True):
            st.dataframe(
                trades,
                use_container_width=True,
                column_config={
                    "timestamp": st.column_config.DatetimeColumn("Timestamp", format="MMM D, YYYY HH:mm"),
                    "price": st.column_config.NumberColumn("Price", format="$%.2f"),
                    "action": st.column_config.TextColumn("Action"),
                },
            )
    else:
        st.markdown('<div class="qc-kpi" style="border-top-color: var(--ink-soft);">No trades were executed for this configuration.</div>',
                    unsafe_allow_html=True)