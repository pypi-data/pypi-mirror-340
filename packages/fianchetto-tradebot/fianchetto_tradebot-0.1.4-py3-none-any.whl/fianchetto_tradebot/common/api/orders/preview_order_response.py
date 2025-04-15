from typing import Optional

from src.fianchetto_tradebot.common.api.orders.order_metadata import OrderMetadata
from src.fianchetto_tradebot.common.api.orders.order_placement_message import OrderPlacementMessage
from src.fianchetto_tradebot.common.api.orders.order_preview import OrderPreview
from src.fianchetto_tradebot.common.api.request_status import RequestStatus
from src.fianchetto_tradebot.common.api.response import Response

class PreviewOrderResponse(Response):
    order_metadata: OrderMetadata
    preview_id: str
    preview_order_info: OrderPreview
    request_status: RequestStatus = RequestStatus.SUCCESS
    order_message: Optional[OrderPlacementMessage] = None
