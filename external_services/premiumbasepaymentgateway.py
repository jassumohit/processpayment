class PremiumBasePaymentGateway:

    def __init__(self, retry=3):
        self.retry = retry

    def process(self, data):
        while self.retry > 0:
            if data is not None:
                return True
            self.retry -= 1
        return False
