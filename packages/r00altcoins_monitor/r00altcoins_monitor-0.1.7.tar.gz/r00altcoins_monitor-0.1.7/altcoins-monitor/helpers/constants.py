from pathlib import Path

SATOSHIS_PER_BTC = 100_000_000
SERVICE = 'coinmarketcap'
MONITOR_COINS = ['BTC/USD', 'DGB/USD', 'FUN/USD', 'RLC/USD', 'MBOX/USD']
_DBDIR = Path('~/.local/share/r00buying_altcoins_monitoring').expanduser().resolve()
_DBDIR.mkdir(exist_ok=True)
DBFILE = _DBDIR / 'data.json'
PERCENT = 20
SLEEP = 1000
