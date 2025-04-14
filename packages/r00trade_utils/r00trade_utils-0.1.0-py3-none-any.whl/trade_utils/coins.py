from .coin import Coin


class Coins:
    def __init__(self):
        self._coins = {}

    def append(self, symbol: str, money: str = None):
        symbol = symbol.upper()
        if symbol not in self._coins:
            self._coins[symbol] = Coin(symbol)

        if money:
            self._coins[symbol].add_money(money)

    def sorted(self):
        return sorted(self._coins.keys())

    def __getitem__(self, symbol) -> Coin:
        symbol = symbol.upper()
        if symbol in self._coins:
            return self._coins[symbol]
        else:
            raise KeyError(f"Coin '{symbol}' not found.")

    def __contains__(self, symbol: str):
        return symbol.upper() in self._coins.keys()

    def __str__(self):
        return ', '.join(str(coin) for coin in self._coins.values())

    def __repr__(self):
        return f'Coins({list(self._coins.keys())})'