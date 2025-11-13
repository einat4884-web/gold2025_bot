from ib_insync import *
import time

HOST = '127.0.0.1'
PORT = 4000
CLIENT_ID = 999

def main():
    ib = IB()
    print(f'Connecting to {HOST}:{PORT} ...')
    ib.connect(HOST, PORT, clientId=CLIENT_ID, readonly=False)
    print('Connected:', ib.isConnected())

    contract = Forex('EURUSD')

    print('Placing test BUY order...')
    order = MarketOrder('BUY', 10000)
    trade = ib.placeOrder(contract, order)

    ib.sleep(2)
    print('Order status:', trade.orderStatus.status)

    print('Done. Check TWS Orders tab!')
    ib.disconnect()

if __name__ == '__main__':
    main()
