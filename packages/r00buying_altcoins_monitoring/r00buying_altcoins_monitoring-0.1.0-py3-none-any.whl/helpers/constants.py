import os

SATOSHIS_PER_BTC = 100_000_000
SERVICE = 'coinmarketcap'
MONITOR_COINS = ['BTC/USD', 'DGB/USD', 'FUN/USD', 'RLC/USD', 'MBOX/USD']
DBFILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data.json")
PERCENT = 20
SLEEP = 1000