from fianchetto_tradebot.common.api.orders.get_order_request import GetOrderRequest
from fianchetto_tradebot.common.api.orders.get_order_response import GetOrderResponse
from fianchetto_tradebot.common.api.orders.order_service import OrderService
from fianchetto_tradebot.common.finance.amount import Amount
from fianchetto_tradebot.common.finance.price import Price
from fianchetto_tradebot.common.order.order_price import OrderPrice
from fianchetto_tradebot.common.order.placed_order import PlacedOrder


class AdjustUntilExecuted():
    def __init__(self, order_service: OrderService, placed_order: PlacedOrder, reserve_price: OrderPrice):
        self.order_service = order_service
        self.placed_order: PlacedOrder = placed_order
        self.order_price: OrderPrice = self.placed_order.order.order_price
        self.reserve_price: OrderPrice = reserve_price
        self.account_id: str = placed_order.placed_order_details.account_id
        self.placed_order_history: list[PlacedOrder] = [placed_order]

    def adjust_order(self):
        placed_order: PlacedOrder = self.get_latest_for_order()
        current_market_price: Price = placed_order.placed_order_details.current_market_price ## TODO: update order to provide this info
        new_order =


    def get_latest_for_order(self)->PlacedOrder:
        exchange_order_id = self.placed_order.order.order_id
        get_order_request = GetOrderRequest(self.account_id, exchange_order_id)
        order_response: GetOrderResponse = self.order_service.get_order(get_order_request)
        self.placed_order_history.append(order_response.placed_order)
        return order_response.placed_order

    def produce_price_delta(self)->Amount:
        # Add this amount to the current price to get the new price
        # Use some kind of heuristic
        pass



