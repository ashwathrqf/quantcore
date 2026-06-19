# 📈 QuantCore

**A Professional Event-Driven Backtesting Engine built in Python**

QuantCore is a modular event-driven backtesting framework inspired by professional trading systems such as Backtrader and QuantConnect. It enables users to test trading strategies on historical market data using a realistic event-driven architecture.

---

## ✨ Features

- 📊 Historical market data using Yahoo Finance
- ⚡ Event-driven architecture
- 📈 Simple Moving Average (SMA) crossover strategy
- 💰 Portfolio management
- 🛒 Order generation and execution
- 💵 Commission and slippage simulation
- 📉 Portfolio equity tracking
- 📊 Performance metrics
  - Total Return
  - Sharpe Ratio
  - Maximum Drawdown
- 📌 Trade history
- 🖥️ Interactive Streamlit dashboard

---

## 🏗️ Project Structure

```
quantcore/
│
├── analytics/
│   └── metrics.py
│
├── data/
│   └── data_handler.py
│
├── events/
│   ├── event.py
│   └── event_queue.py
│
├── execution/
│   └── execution.py
│
├── portfolio/
│   └── portfolio.py
│
├── strategy/
│   ├── base.py
│   └── sma.py
│
├── engine.py
│
app.py
```

---

## 🔄 Architecture

```
Historical Data
       │
       ▼
Data Handler
       │
       ▼
Market Event
       │
       ▼
Strategy
       │
       ▼
Signal Event
       │
       ▼
Portfolio
       │
       ▼
Order Event
       │
       ▼
Execution Handler
       │
       ▼
Fill Event
       │
       ▼
Portfolio Update
       │
       ▼
Performance Metrics
```

---

## 📊 Dashboard

The Streamlit dashboard includes:

- Backtest configuration
- Strategy parameters
- Execution parameters
- Performance metrics
- Portfolio equity curve
- Trade history

---

## 🚀 Installation

Clone the repository

```bash
git clone https://github.com/ashwathrqf/event_backtester.git
cd event_backtester
```

Create a virtual environment

```bash
python -m venv .venv
```

Activate

Windows

```bash
.venv\Scripts\activate
```

Linux / macOS

```bash
source .venv/bin/activate
```

Install dependencies

```bash
pip install -r requirements.txt
```

---

## ▶️ Run

```bash
streamlit run app.py
```

---

## 🛠️ Tech Stack

- Python
- Streamlit
- Pandas
- NumPy
- Plotly
- yFinance

---

## 📌 Future Improvements

- Multiple trading strategies
- Multi-asset portfolios
- Risk management module
- Position sizing algorithms
- Additional performance metrics
- Buy & Hold benchmark
- Walk-forward optimization

---

## 👨‍💻 Author

**Ashwath R**

Mechanical Engineering  
Indian Institute of Technology Madras

---

## ⭐ If you found this project useful, consider starring the repository.