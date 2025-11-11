# paper_test_trade.py — BUY ואז SELL בדמו (EURUSD) דרך IB Gateway על פורט 4000
from ib_insync import *
import asyncio

HOST = "127.0.0.1"
PORT = 4000         # מותאם להגדרה אצלך
CLIENT_ID = 1

async def main():
    ib = IB()
    print(f"Connecting {HOST}:{PORT} ...")
    await ib.connectAsync(HOST, PORT, clientId=CLIENT_ID, timeout=10)
    print("Connected ?")

    contract = Forex('EURUSD')
    qty = 10000  # 10K units

    # BUY
    buy = ib.placeOrder(contract, MarketOrder('BUY', qty))
    while not buy.isDone():
        await asyncio.sleep(0.2)
    print("BUY:", buy.orderStatus.status, "filled:", buy.orderStatus.filled)

    await asyncio.sleep(2)

    # SELL (סגירת הפוזיציה)
    sell = ib.placeOrder(contract, MarketOrder('SELL', qty))
    while not sell.isDone():
        await asyncio.sleep(0.2)
    print("SELL:", sell.orderStatus.status, "filled:", sell.orderStatus.filled)

    print("Done ?")
    await ib.disconnectAsync()

if __name__ == "__main__":
    asyncio.run(main())
