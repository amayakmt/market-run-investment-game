from config import FEE_MIN, FEE_RATE
def compute_fee(price: float, quantity: float) -> float:
    return max(FEE_MIN, price * quantity * FEE_RATE)