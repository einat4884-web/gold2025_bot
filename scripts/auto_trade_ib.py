
import os, time
from datetime import datetime
from dotenv import load_dotenv
from ib_insync import IB, Forex, Stock, Future, util, Contract, MarketOrder, LimitOrder, StopOrder
import pandas as pd

load_dotenv()
ROOT = os.path.dirname(__file__)
DATA_DIR = os.path.join(os.path.dirname(ROOT), 'data') if os.path.basename(ROOT) == 'scripts' else os.path.join(ROOT, 'data')
LOGS_DIR = os.path.join(os.path.dirname(ROOT), 'logs') if os.path.basename(ROOT) == 'scripts' else os.path.join(ROOT, 'logs')
os.makedirs(DATA_DIR, exist_ok=True)
os.makedirs(LOGS_DIR, exist_ok=True)
TRADES_CSV = os.path.join(DATA_DIR, 'trades_log.csv')

def env(name, default=None):
    v = os.getenv(name, default)
    return v if v is not None else default

def append_trade(row: dict):
    df = pd.DataFrame([row])
    if not os.path.exists(TRADES_CSV) or os.path.getsize(TRADES_CSV) == 0:
        df.to_csv(TRADES_CSV, index=False)
    else:
        df.to_csv(TRADES_CSV, mode='a', header=False, index=False)

def build_contract():
    symbol   = (env("SYMBOL","EURUSD") or "EURUSD").strip()
    sectype  = (env("SECTYPE","FOREX") or "FOREX").upper()
    exchange = (env("EXCHANGE","IDEALPRO") or "IDEALPRO")
    currency = (env("CURRENCY","USD") or "USD")
    month    = env("CONTRACT_MONTH","") or ""
    if sectype == "FOREX":
        return Forex(symbol)
    elif sectype == "STK":
        return Stock(symbol, exchange, currency)
    elif sectype == "FUT":
        if not month:
            raise ValueError("CONTRACT_MONTH (YYYYMM) is required for futures.")
        return Future(symbol=symbol, exchange=exchange, currency=currency, lastTradeDateOrContractMonth=month)
    else:
        c = Contract()
        c.symbol = symbol
        c.secType = sectype
        c.exchange = exchange
        c.currency = currency
        return c

def main():
    mode = (env("IBKR_MODE","paper") or "paper").lower()
    host = env("IBKR_HOST","127.0.0.1")
    port = int(env("IBKR_PORT","7497"))
    client_id = int(env("IBKR_CLIENT_ID","1"))
    DRY_RUN = (env("DRY_RUN","false") or "false").lower() == "true"

    ib = IB()
    print(f"Connecting {host}:{port}? clientId={client_id} | mode={mode} | DRY_RUN={DRY_RUN}")
    ib.connect(host, port, clientId=client_id, readonly=DRY_RUN)
    print("Connected:", ib.isConnected())

    acct = ib.managedAccounts()[0] if ib.managedAccounts() else None
    print("Account:", acct)

    contract = build_contract()
    print("Contract:", contract)
    ticker = ib.reqMktData(contract, "", False, False)
    util.sleep(1.0)
    price = ticker.marketPrice()
    if price is None or not isinstance(price, (int, float)) or price <= 0:
        price = 1.1 if (env("SECTYPE","FOREX") or "FOREX").upper() == "FOREX" else 100.0
        print(f"[INFO] Using fallback price for DRY_RUN/weekend: {price}")

    # Risk
    eq = 10000.0
    try:
        for v in ib.accountValues():
            if v.tag == "NetLiquidation" and (acct is None or v.account == acct):
                eq = float(v.value); break
    except Exception as e:
        print("[WARN] Could not read NetLiquidation:", e)
    risk_pct = float(env("RISK_PCT","0.01"))
    tp_pct   = float(env("TP_PCT","0.004"))
    sl_pct   = float(env("SL_PCT","0.003"))
    stop_distance = sl_pct * float(price)
    risk_dollars = eq * risk_pct
    qty = max(1, int(risk_dollars / stop_distance)) if stop_distance > 0 else 1
    side = "BUY"

    order_id = None
    if DRY_RUN:
        print("[DRY-RUN] Skipping order placement.")
        order_id = f"DRY_{int(time.time())}"
    else:
        # Parent market order, two children (TP/SL)
        parent = MarketOrder(side, qty, transmit=False)
        tp = LimitOrder("SELL" if side=="BUY" else "BUY",
                        qty, float(price) * (1+tp_pct if side=="BUY" else 1-tp_pct),
                        transmit=False)
        sl = StopOrder("SELL" if side=="BUY" else "BUY",
                       qty, float(price) * (1-sl_pct if side=="BUY" else 1+sl_pct),
                       transmit=True)

        # Place parent
        trade = ib.placeOrder(contract, parent)
        order_id = trade.order.orderId
        # Link children by setting parentId on order objects
        tp.parentId = order_id
        sl.parentId = order_id
        # Send children
        ib.placeOrder(contract, tp)
        ib.placeOrder(contract, sl)
        print("Orders submitted. ParentId:", order_id)

    append_trade({
        "timestamp": datetime.utcnow().isoformat(),
        "symbol": env("SYMBOL","EURUSD"),
        "side": side,
        "qty": qty,
        "entry_price": round(float(price),6),
        "exit_price": "",
        "pnl": "",
        "status": "dry-run" if DRY_RUN else "submitted",
        "order_id": order_id
    })

    print("Running... Press Ctrl+C to exit.")
    try:
        while True:
            ib.waitOnUpdate(timeout=1)
    except KeyboardInterrupt:
        pass
    finally:
        ib.disconnect()
        print("Disconnected.")

if __name__ == "__main__":
    main()
