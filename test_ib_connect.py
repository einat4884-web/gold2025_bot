from ib_insync import IB

try:
    ib = IB()
    print("Connecting to IBKR...")
    ib.connect('127.0.0.1', 7497, clientId=1, readonly=True)
    print("Connected:", ib.isConnected())
    print("Managed accounts:", ib.managedAccounts())
    vals = [v for v in ib.accountValues() if v.tag == "NetLiquidation"]
    print("NetLiquidation:", [(v.acc, v.value, v.currency) for v in vals[:3]])
finally:
    ib.disconnect()
    print("Disconnected.")
