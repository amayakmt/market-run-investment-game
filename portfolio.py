from dataclasses import dataclass, field
from config import STARTING_CASH
from fees import compute_fee
from orders import Order

@dataclass
class Position:
    average_price: float = 0
    quantity: float = 0
    reserved_quantity: float = 0

@dataclass
class Portfolio:
    username: str
    cash: float = STARTING_CASH
    reserved_cash: float = 0
    _next_order_id: int = 1
    orders: list = field(default_factory=list)
    positions: dict[str, Position] = field(default_factory=dict)
    realized_pnl: float = 0
    dividends_received: float = 0
    fees_paid: float = 0

    # GET CASH|QUANTITY ---------------------------------------------------------------------

    def get_available_cash(self) -> float:
        return self.cash - self.reserved_cash
    
    def get_available_quantity(self, ticker: str) -> float:
        if ticker not in self.positions:
            return 0
        return self.positions[ticker].quantity - self.positions[ticker].reserved_quantity

    # PLACE ORDER -----------------------------------------------------------------------------

    def place_order(self, order: Order, current_price: float | None = None) -> None:
        if order.order_type == "MARKET":
            self.place_market_order(order, current_price)
            return

        self.place_limit_order(order)
        return

    def place_market_order(self, order: Order, current_price):
        if current_price is None:
            raise ValueError("Market order requires current_price")

        cost = order.quantity * current_price + compute_fee(current_price, order.quantity)
        if order.side == "BUY" and self.get_available_cash() < cost:
            raise ValueError(f'insufficient cash: ${self.get_available_cash()}. order cost: ${cost}.') 
        if order.side == "SELL" and self.get_available_quantity(order.ticker) < order.quantity:
            raise ValueError(f'insufficient quantity: {self.get_available_quantity(order.ticker)}. order quantity: {order.quantity}.')

        if order.side == "BUY":
            self.buy_shares(order.ticker, current_price, order.quantity)
        else:
            self.sell_shares(order.ticker, current_price, order.quantity)
        print(f'Market order placed: {order.ticker} @{current_price} x {order.quantity} shares. (${current_price * order.quantity} total)')
        return
    
    def place_limit_order(self, order: Order):
        if order.limit_price is None:
            raise ValueError("Limit order requires limit_price.")

        cost = order.quantity * order.limit_price + compute_fee(order.limit_price, order.quantity) # worst-case cost at limit
        if order.side == "BUY" and self.get_available_cash() < cost:
            raise ValueError(f'insufficient cash: ${self.get_available_cash()}. order cost: ${cost}.') 
        if order.side == "SELL" and self.get_available_quantity(order.ticker) < order.quantity:
            raise ValueError(f'insufficient quantity: {self.get_available_quantity(order.ticker)}. order quantity: {order.quantity}.')
        
        if order.side == "BUY":
            self.reserved_cash += cost
            order.reserved_cash = cost
        else:
            self.positions[order.ticker].reserved_quantity += order.quantity

        order.order_id = self._next_order_id
        self._next_order_id += 1
        self.orders.append(order)
        print(f'Limit order placed: {order.ticker} @{order.limit_price} x {order.quantity} shares. (${order.reserved_cash} total)')
        return

    # CANCEL ORDER -----------------------------------------------------------------------

    def cancel_order(self, order_id: int) -> None:
        order = next((o for o in self.orders if o.order_id == order_id), None)
        if order is None:
            raise ValueError(f"No open order with id {order_id}.")

        if order.side == "BUY":
            self.reserved_cash -= order.reserved_cash
        else:
            self.positions[order.ticker].reserved_quantity -= order.quantity
        
        self.orders.remove(order)
        print(f'Limit order {order_id} successfully cancelled.')
        return

    # FILL ORDER --------------------------------------------------------------------------------

    def fill_order(self, order: Order, price: float) -> None:
        if order.side == "BUY" and price > order.limit_price:
            raise ValueError(f'Buy limit at ${order.limit_price} can not fill above ${price}')
        if order.side == "SELL" and price < order.limit_price:
            raise ValueError(f'Sell limit at ${order.limit_price} cannot fill below ${price}')

        if order.side == "BUY":
            self.reserved_cash -= order.reserved_cash
            self.buy_shares(order.ticker, price, order.quantity)
        else:
            self.positions[order.ticker].reserved_quantity -= order.quantity
            self.sell_shares(order.ticker, price, order.quantity)

        print(f'Limit order for {order.order_id} was filled at ${price}.')
        self.orders.remove(order)
        return

    # BUY|SELL SHARES ----------------------------------------------------------------------

    def buy_shares(self, ticker, buy_price, buy_quantity):
        position = self.positions.setdefault(ticker, Position())
        position.average_price = (position.average_price * position.quantity + buy_price * buy_quantity) / (position.quantity + buy_quantity)
        position.quantity += buy_quantity

        fees = compute_fee(buy_price, buy_quantity)
        self.fees_paid += fees
        self.cash -= (buy_price * buy_quantity) + fees

    def sell_shares(self, ticker, sell_price, sell_quantity):
        position = self.positions[ticker]
        position.quantity -= sell_quantity

        self.realized_pnl += (sell_price - position.average_price) * sell_quantity

        if position.quantity == 0:
            del self.positions[ticker]
        
        fees = compute_fee(sell_price, sell_quantity)
        self.fees_paid += fees
        self.cash += (sell_price * sell_quantity) - fees

    # GET UNREALIZED P&L --------------------------------------------------------------------------

    def get_unrealized_pnl(self, current_price: dict[str, float]) -> float:
        unrealized_pnl = 0
        for ticker, position in self.positions.items():
            if ticker not in current_price:
                continue
            unrealized_pnl += (current_price[ticker] - position.average_price) * position.quantity
        return unrealized_pnl
