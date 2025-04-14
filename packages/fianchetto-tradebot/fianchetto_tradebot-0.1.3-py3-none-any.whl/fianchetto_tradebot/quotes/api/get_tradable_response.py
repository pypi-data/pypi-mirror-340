from datetime import datetime
from typing import Optional

from pydantic import BaseModel

from src.fianchetto_tradebot.common.api.finance.greeks.greeks import Greeks
from src.fianchetto_tradebot.common.finance.price import Price
from src.fianchetto_tradebot.common.finance.tradable import Tradable
from src.fianchetto_tradebot.common.api.response import Response


class GetTradableResponse(Response, BaseModel):
    tradable: Tradable
    response_time: Optional[datetime] = None
    current_price: Price
    volume: int
    greeks: Optional[Greeks] = None
