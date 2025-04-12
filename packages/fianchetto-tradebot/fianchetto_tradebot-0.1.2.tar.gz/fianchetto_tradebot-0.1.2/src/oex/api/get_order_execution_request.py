from common import Request


class GetOrderExecutionRequest(Request):
    def __init__(self, managed_order_id: str):
        self.managed_order_id: str = managed_order_id


