from common.finance.option import Option
from common.finance.tradable import Tradable


class PricedOption(Tradable):
    option: Option

    def copy_of(self):
        return PricedOption(option=self.option, price=self.price)
