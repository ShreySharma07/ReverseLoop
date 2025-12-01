from decimal import Decimal, ROUND_HALF_UP
# from dotenv import load_env
from reverse_loop.config import settings

class ProfitCalculator:

    @staticmethod
    def calculate_shipping(weight_lbs: float)->Decimal:
        if weight_lbs < 1.0:
            return Decimal("5.00")
        elif weight_lbs < 5.0:
            return Decimal("12.00")
        else:
            return Decimal("20.00")
    
    @classmethod
    def calculate_net_profit(cls, market_price: float, weight_lbs: float) -> dict:

        price = Decimal(str(market_price))

        platform_fee = (price * settings.EBAY_FEE_PERCENT).quantize(Decimal("0.01"), rounding = ROUND_HALF_UP)

        profit = price - platform_fee - cls.calculate_shipping(weight_lbs) - settings.HANDLING_COST

        return {
            "market_price": float(price),
            "platform_fee": float(platform_fee),
            "shipping_cost": float(cls.calculate_shipping(weight_lbs)),
            "handling_cost": float(settings.HANDLING_COST),
            "net_profit": float(profit),
            "is_profitable": profit > 0
        }