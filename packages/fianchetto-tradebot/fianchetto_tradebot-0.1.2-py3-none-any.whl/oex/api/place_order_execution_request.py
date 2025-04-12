from common import Request
from common import Order


class PlaceOrderExecutionRequest(Request):
    def __init__(self, order: Order):
        self.order = order


