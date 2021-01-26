from decimal import Decimal
from .cheapbasepaymentgateway import CheapBasePaymentGateway
from .expensivebasepaymentgateway import ExpensiveBasePaymentGateway
from .premiumbasepaymentgateway import PremiumBasePaymentGateway


class externalServices:

    def __init__(self, data):
        self.data = data

    def make_payment(self):
        try:
            amount = Decimal(self.data['Amount'])
            if amount <= 20:
                mode = CheapBasePaymentGateway()
            elif 20 < amount <= 500:
                mode = ExpensiveBasePaymentGateway()
            elif amount > 500:
                mode = PremiumBasePaymentGateway()
            else:
                return False

            status = mode.process(self.data)
            return status
        except:
            return False
