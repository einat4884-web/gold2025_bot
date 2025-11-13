from ib_insync import *
import time

HOST = '127.0.0.1'
PORT = 4000
CLIENT_ID = 998

def main():
    ib = IB()
    print(f'Connecting to {HOST}:{PORT} ...')
    ib.connect(HOST, PORT, clientId=CLIENT_ID, readonly=False)
    print('Connected:', ib.isConnected())

    contract = Stock('NVDA', 'SMART', 'USD')

    print('Placing test BUY order on NVDA...')
    order = MarketOrder('BUY', 1)
    trade = ib.placeOrder(contract, order)

    ib.sleep(3)
    print('Order status:', trade.orderStatus.status)

    print('Done. Check TWS Orders tab!')
    ib.disconnect()

if __name__ == '__main__':
    main()
