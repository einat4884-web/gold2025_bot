from ib_insync import *


yes
from ib_insync import *

HOST="127.0.0.1"; PORT=4000; CLIENT_ID=1
ib=IB()
try:
    print(f"Connecting {HOST}:{PORT} ...")
    ib.connect(HOST, PORT, clientId=CLIENT_ID, readonly=False)
    print("Connected")

    c=Forex("EURUSD"); qty=10000
    b=ib.placeOrder(c, MarketOrder("BUY", qty))
    while not b.isDone(): ib.sleep(0.2)
    print("BUY:", b.orderStatus.status, "filled:", b.orderStatus.filled)

    ib.sleep(1)
    s=ib.placeOrder(c, MarketOrder("SELL", qty))
    while not s.isDone(): ib.sleep(0.2)
    print("SELL:", s.orderStatus.status, "filled:", s.orderStatus.filled)
    print("Done")
finally:
    ib.disconnect()
