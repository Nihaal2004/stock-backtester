# src/app.py
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

st.set_page_config(page_title="Stock Strategy Backtester Lite", layout="wide")
st.title("Stock Strategy Backtester Lite")
st.caption("Educational use only. Not financial advice. Trades execute on next-day close (no lookahead bias).")

# ----------------------------
# Helpers
# ----------------------------
def sma(series: pd.Series, window: int) -> pd.Series:
    return series.rolling(window, min_periods=window).mean()

def rsi(close: pd.Series, period: int = 14) -> pd.Series:
    delta = close.diff()
    gain = delta.clip(lower=0)
    loss = (-delta).clip(lower=0)
    avg_gain = gain.rolling(period, min_periods=period).mean()
    avg_loss = loss.rolling(period, min_periods=period).mean()
    rs = avg_gain / (avg_loss + 1e-12)
    return 100 - (100 / (1 + rs))

def max_drawdown(equity: pd.Series) -> float:
    peak = equity.cummax()
    dd = (equity - peak) / peak
    return float(dd.min()) if len(dd) else 0.0

def cagr(equity: pd.Series, dates: pd.Series) -> float:
    if len(equity) < 2:
        return np.nan
    days = (dates.iloc[-1] - dates.iloc[0]).days
    if days <= 0:
        return np.nan
    years = days / 365.25
    return float((equity.iloc[-1] / equity.iloc[0]) ** (1 / years) - 1)

def load_and_clean_csv(uploaded_file) -> pd.DataFrame:
    df = pd.read_csv(uploaded_file)
    # Accept common variations
    col_map = {c: c.strip() for c in df.columns}
    df = df.rename(columns=col_map)

    required = {"Date", "Close"}
    if not required.issubset(df.columns):
        missing = sorted(list(required - set(df.columns)))
        raise ValueError(f"Missing required columns: {missing}. Required: Date, Close")

    df["Date"] = pd.to_datetime(df["Date"], errors="coerce")
    df["Close"] = pd.to_numeric(df["Close"], errors="coerce")

    df = df.dropna(subset=["Date", "Close"]).copy()
    df = df.sort_values("Date").reset_index(drop=True)

    if len(df) < 10:
        raise ValueError("Not enough valid rows after cleaning. Provide at least 10 rows.")

    return df

# ----------------------------
# Sidebar: Data
# ----------------------------
st.sidebar.header("1) Data")
uploaded = st.sidebar.file_uploader("Upload CSV (required: Date, Close)", type=["csv"])

if uploaded is None:
    st.info("Upload a CSV to continue. Required columns: Date, Close.")
    st.stop()

try:
    df = load_and_clean_csv(uploaded)
except Exception as e:
    st.error(str(e))
    st.stop()

st.sidebar.success(f"Loaded {len(df)} rows")
st.write("Preview (last 10 rows)")
st.dataframe(df.tail(10), use_container_width=True)

# Optional: Date range filter (small + useful)
st.sidebar.header("Optional: Date Range")
min_d, max_d = df["Date"].iloc[0], df["Date"].iloc[-1]
date_range = st.sidebar.date_input("Backtest range", value=(min_d.date(), max_d.date()))
if isinstance(date_range, tuple) and len(date_range) == 2:
    start_date = pd.to_datetime(date_range[0])
    end_date = pd.to_datetime(date_range[1])
    df = df[(df["Date"] >= start_date) & (df["Date"] <= end_date)].copy().reset_index(drop=True)

if len(df) < 10:
    st.error("Selected date range leaves too few rows. Expand the range.")
    st.stop()

# ----------------------------
# Sidebar: Strategy (FORM to prevent rerun resets)
# ----------------------------
st.sidebar.header("2) Strategy")

with st.sidebar.form("backtest_form"):
    strategy = st.selectbox("Choose strategy", ["SMA Crossover", "RSI Threshold"])

    initial_capital = st.number_input("Initial capital", min_value=1000, value=100000, step=1000)
    cost_pct = st.number_input("Transaction cost per trade (%)", min_value=0.0, max_value=5.0, value=0.4, step=0.1)
    cost = cost_pct / 100.0

    # Strategy params
    if strategy == "SMA Crossover":
        # Safe defaults for small datasets
        fast = st.number_input("Fast SMA", min_value=2, value=3, step=1)
        slow = st.number_input("Slow SMA", min_value=3, value=8, step=1)
    else:
        period = st.number_input("RSI Period", min_value=2, value=14, step=1)
        buy_th = st.number_input("Buy when RSI < ", min_value=1, max_value=99, value=30, step=1)
        sell_th = st.number_input("Sell when RSI > ", min_value=1, max_value=99, value=70, step=1)

    run = st.form_submit_button("Run Backtest")

if not run:
    st.info("Set parameters in the sidebar and click **Run Backtest**.")
    st.stop()

# ----------------------------
# Backtest
# ----------------------------
df_bt = df.copy()
close = df_bt["Close"]

if strategy == "SMA Crossover":
    if fast >= slow:
        st.error("Fast SMA must be less than Slow SMA.")
        st.stop()
    if len(df_bt) < slow + 2:
        st.error(f"Not enough rows ({len(df_bt)}) for Slow SMA={slow}. Use smaller windows or more data.")
        st.stop()

    df_bt["fast"] = sma(close, int(fast))
    df_bt["slow"] = sma(close, int(slow))
    df_bt["signal"] = (df_bt["fast"] > df_bt["slow"]).astype(int)

else:
    if buy_th >= sell_th:
        st.error("Buy threshold must be less than Sell threshold.")
        st.stop()
    if len(df_bt) < period + 2:
        st.error(f"Not enough rows ({len(df_bt)}) for RSI period={period}. Use smaller period or more data.")
        st.stop()

    df_bt["rsi"] = rsi(close, int(period))

    # Simple position state machine
    in_pos = 0
    pos = []
    for v in df_bt["rsi"].fillna(50):
        if in_pos == 0 and v < buy_th:
            in_pos = 1
        elif in_pos == 1 and v > sell_th:
            in_pos = 0
        pos.append(in_pos)
    df_bt["signal"] = pos

# Next-day execution: position(t) = signal(t-1)
df_bt["position"] = df_bt["signal"].shift(1).fillna(0).astype(int)

# Returns
df_bt["ret"] = close.pct_change().fillna(0.0)
df_bt["strategy_ret"] = df_bt["position"] * df_bt["ret"]

# Transaction costs on position changes (entry/exit)
df_bt["trade_flag"] = df_bt["position"].diff().abs().fillna(0).astype(int)
df_bt["strategy_ret"] = df_bt["strategy_ret"] - (df_bt["trade_flag"] * cost)

# Equity curve
df_bt["equity"] = float(initial_capital) * (1 + df_bt["strategy_ret"]).cumprod()

# Trade log (entry/exit based on position transitions)
trades = []
pos_prev = df_bt["position"].shift(1).fillna(0).astype(int)
enter = (pos_prev == 0) & (df_bt["position"] == 1)
exit_ = (pos_prev == 1) & (df_bt["position"] == 0)

entry_idx = list(df_bt.index[enter])
exit_idx = list(df_bt.index[exit_])

# If we enter and never exit, ignore the open trade for log (keeps it simple)
for ei in entry_idx:
    xo = [x for x in exit_idx if x > ei]
    if not xo:
        break
    xi = xo[0]
    entry_date = df_bt.loc[ei, "Date"]
    exit_date = df_bt.loc[xi, "Date"]
    entry_price = df_bt.loc[ei, "Close"]
    exit_price = df_bt.loc[xi, "Close"]
    pnl_pct = (exit_price / entry_price) - 1
    trades.append([entry_date, exit_date, entry_price, exit_price, pnl_pct])
    exit_idx.remove(xi)

trades_df = pd.DataFrame(trades, columns=["Entry Date", "Exit Date", "Entry", "Exit", "P/L %"])
if not trades_df.empty:
    trades_df["P/L %"] = (trades_df["P/L %"] * 100).round(2)
    win_rate = float((trades_df["P/L %"] > 0).mean())
else:
    win_rate = np.nan

# Metrics
total_return = float(df_bt["equity"].iloc[-1] / df_bt["equity"].iloc[0] - 1)
metric_cagr = cagr(df_bt["equity"], df_bt["Date"])
mdd = max_drawdown(df_bt["equity"])

# Guard: no trades case
days_in_position = int(df_bt["position"].sum())
if days_in_position == 0:
    st.warning("No trades were generated with the current parameters. Try smaller SMA windows or different RSI thresholds.")

# ----------------------------
# UI Output
# ----------------------------
left, right = st.columns([2, 1])

with left:
    st.subheader("Equity Curve")
    fig, ax = plt.subplots()
    ax.plot(df_bt["Date"], df_bt["equity"])
    ax.set_xlabel("Date")
    ax.set_ylabel("Equity")
    st.pyplot(fig, clear_figure=True)

with right:
    st.subheader("Key Metrics")
    st.metric("Total Return", f"{total_return*100:.2f}%")
    st.metric("CAGR", f"{metric_cagr*100:.2f}%" if pd.notna(metric_cagr) else "N/A")
    st.metric("Max Drawdown", f"{mdd*100:.2f}%")
    st.metric("Win Rate", f"{win_rate*100:.2f}%" if pd.notna(win_rate) else "N/A")
    st.metric("# Trades", f"{len(trades_df)}")

st.subheader("Trades")
st.dataframe(trades_df, use_container_width=True)
