import datetime

from common.finance.amount import Amount
from common.finance.currency import Currency
from common.finance.equity import Equity
from common.finance.option import Option
from common.finance.exercise_style import ExerciseStyle
from common.finance.option_type import OptionType
from common.finance.tradable import Tradable
from common.order.action import Action
from common.order.expiry.good_for_day import GoodForDay
from common.order.expiry.order_expiry import OrderExpiry
from common.order.order import Order
from common.order.order_line import OrderLine
from common.order.order_price import OrderPrice
from common.order.order_price_type import OrderPriceType

e: Equity = Equity(ticker="GE", company_name="General Electric")


def test_build_single_line_order():
    strike: Amount = Amount(whole=10,part=0, currency=Currency.US_DOLLARS)

    order_id: str = "123"
    order_expiry: OrderExpiry = GoodForDay()
    call_option: Tradable = Option(equity=e, type=OptionType.CALL, strike=strike, expiry=datetime.datetime(2024, 11, 5).date(), style=ExerciseStyle.AMERICAN)
    order_line = OrderLine(tradable=call_option,  action=Action.SELL_OPEN, quantity=1)
    order_price: OrderPrice = OrderPrice(order_price_type=OrderPriceType.NET_CREDIT, price=Amount(whole=0, part=14, currency=Currency.US_DOLLARS))

    single_order = Order(expiry=order_expiry, order_lines=[order_line], order_price=order_price)

    assert single_order is not None


def test_build_dual_line_order():
    strike: Amount = Amount(whole=10, part=0, currency=Currency.US_DOLLARS)

    order_expiry: OrderExpiry = GoodForDay()
    call_option: Tradable = Option(equity=e, type=OptionType.CALL, strike=strike, expiry=datetime.datetime(2024, 11, 5).date(),
                                   style=ExerciseStyle.AMERICAN)
    order_line = OrderLine(tradable=call_option, action=Action.SELL_OPEN, quantity=2)

    strike2: Amount = Amount(whole=20, part=0, currency=Currency.US_DOLLARS)
    call_option2 = Option(equity=e, type=OptionType.CALL, strike=strike2, expiry=datetime.date(2024, 11, 5), style=ExerciseStyle.AMERICAN)
    order_line2 = OrderLine(tradable=call_option2, action=Action.BUY_OPEN, quantity=1)

    order_price: OrderPrice = OrderPrice(order_price_type=OrderPriceType.NET_CREDIT, price=Amount(whole=0, part=14, currency=Currency.US_DOLLARS))

    dual_order = Order(expiry=order_expiry, order_lines=[order_line, order_line2], order_price=order_price)

    assert dual_order is not None