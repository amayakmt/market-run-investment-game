from dataclasses import dataclass, field
from config import STARTING_CASH, FEE_MIN, FEE_RATE

@dataclass
class Position:
    average_price: float = 0
    quantity: float = 0

@dataclass
class Portfolio:
    username: str
    positions: dict[str, Position] = field(default_factory=dict)
    cash: float = STARTING_CASH
    realized_pnl: float = 0
    dividends_received: float = 0
    fees_paid: float = 0

    def buy_shares(self, ticker, buy_price, buy_quantity):
        position = self.positions.setdefault(ticker, Position())
        position.average_price = (position.average_price * position.quantity + buy_price * buy_quantity) / (position.quantity + buy_quantity)
        position.quantity += buy_quantity

        fees = max(FEE_MIN, buy_price * buy_quantity * FEE_RATE)
        self.fees_paid += fees
        self.cash -= (buy_price * buy_quantity) + fees

    def sell_shares(self, ticker, sell_price, sell_quantity):
        position = self.positions[ticker]
        position.quantity -= sell_quantity

        self.realized_pnl += (sell_price - position.average_price) * sell_quantity

        if position.quantity == 0:
            del self.positions[ticker]
        
        fees = max(FEE_MIN, sell_price * sell_quantity * FEE_RATE)
        self.fees_paid += fees
        self.cash += (sell_price * sell_quantity) - fees

    def get_unrealized_pnl(self, current_price: dict[str, float]) -> float:
        unrealized_pnl = 0
        for ticker, position in self.positions.items():
            if ticker not in current_price:
                continue
            unrealized_pnl += (current_price[ticker] - position.average_price) * position.quantity
        return unrealized_pnl
