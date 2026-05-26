from dataclasses import dataclass
from config import GTC_EXPIRY_WEEKS

@dataclass
class Order:
    side: str # BUY | SELL
    ticker: str
    quantity: float
    order_type: str # MARKET | LIMIT
    limit_price: float | None
    reserved_cash: float = 0
    order_id: int = 0
    weeks_until_expiry: int = GTC_EXPIRY_WEEKS

    def __post_init__(self):
        if self.side not in {"BUY", "SELL"}:
            raise ValueError("Order side must be 'BUY' or 'SELL'")
        if self.order_type not in {"MARKET", "LIMIT"}:
            raise ValueError("Order type must be 'MARKET' or 'LIMIT'")
        if self.quantity <= 0:
            raise ValueError("Order quantity must be above 0")
        if self.order_type == "LIMIT" and self.limit_price is None:
            raise ValueError("Limit order must have a limit price")
        if self.order_type == "LIMIT" and self.limit_price <= 0:
            raise ValueError("Limit order must have a limit price above 0")
            