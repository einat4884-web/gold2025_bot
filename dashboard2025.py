import os
import pandas as pd
import streamlit as st

st.set_page_config(page_title="Gold2025 – IBKR Dashboard", layout="wide")

DATA_DIR = os.path.join(os.path.dirname(__file__), 'data')
TRADES_CSV = os.path.join(DATA_DIR, 'trades_log.csv')

st.title("📈 Gold2025 – Live Trades (IBKR)")

# Side bar
st.sidebar.header("Controls")
refresh = st.sidebar.number_input("Auto-refresh (seconds)", min_value=2, max_value=60, value=5, step=1)
st.sidebar.write("Make sure `auto_trade_ib.py` is running.")

# Load trades
if os.path.exists(TRADES_CSV) and os.path.getsize(TRADES_CSV) > 0:
    df = pd.read_csv(TRADES_CSV)
    st.subheader("Trades log")
    st.dataframe(df.tail(200), use_container_width=True)

    # Equity curve (naive cum PnL)
    if "pnl" in df.columns:
        pnl = pd.to_numeric(df["pnl"], errors="coerce").fillna(0.0)
        eq = pnl.cumsum()
        eq.index = range(len(eq))
        st.subheader("PnL cumulative (simulated)")
        st.line_chart(eq)
else:
    st.info("No trades yet. Once orders are submitted, they will appear here.")

# Auto-refresh
st.rerun()
