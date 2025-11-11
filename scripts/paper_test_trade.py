from ib_insync import *

HOST = "127.0.0.1"
PORT = 4000
CLIENT_ID = 1

ib = IB()
try:
    print(f"Connecting {HOST}:{PORT} ...")
    ib.connect(HOST, PORT, clientId=CLIENT_ID, readonly=False)
    print("Connected")

    # Pick Paper account explicitly
    accts = ib.managedAccounts()
    acct = accts[0] if accts else ""
    print("Account:", acct)

    # Contract
    c = Forex("EURUSD")
    qty = 10000

    # BUY with explicit TIF and account
    buy_order = MarketOrder("BUY", qty, tif="DAY")
    buy_order.account = acct
    b = ib.placeOrder(c, buy_order)
    while not b.isDone():
        ib.sleep(0.2)
    print("BUY:", b.orderStatus.status, "f