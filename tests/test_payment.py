import pytest, sys
from pathlib import Path

flask_app_root = str(Path(__file__).resolve().parent.parent)
sys.path.insert(0, str(flask_app_root))

from app import app


class TestProcessPayment:

    def test_no_data(self, client):
        res = client.get('/payment/pay')
        assert res.status_code == 400

    def test_invalid_ccnumber(self, client):
        res = client.get('/payment/pay?CreditCardNumber=412111-1111-1111-111122&CardHolder=mohit&'
                         'ExpirationDate=27/1/2022&SecurityCode=785&Amount=8.54')
        assert res.status_code == 400

    def test_invalid_ccnumber_format(self, client):
        res = client.get('/payment/pay?CreditCardNumber=4a11-1111-1111-1111&CardHolder=mohit&'
                         'ExpirationDate=27/1/2022&SecurityCode=785&Amount=8.54')
        assert res.status_code == 400

    def test_empty_cardholder(self, client):
        res = client.get(
            '/payment/pay?CreditCardNumber=4111-1111-1111-1111&CardHolder=&ExpirationDate=27/1/2022&'
            'SecurityCode=785&Amount=8.54')
        assert res.status_code == 400

    def test_invalid_datetime_format(self, client):
        res = client.get(
            '/payment/pay?CreditCardNumber=4111-1111-1111-1111&CardHolder=mohit&ExpirationDate=11/25/25&'
            'SecurityCode=785&Amount=8.54')
        assert res.status_code == 400

    def test_invalid_datetime_past(self, client):
        res = client.get(
            '/payment/pay?CreditCardNumber=4111-1111-1111-1111&CardHolder=mohit&'
            'ExpirationDate=11/2/2020&SecurityCode=785&Amount=8.54')
        assert res.status_code == 400

    def test_invalid_cvv_length(self, client):
        res = client.get(
            '/payment/pay?CreditCardNumber=4111-1111-1111-1111&CardHolder=mohit&'
            'ExpirationDate=11/2/2022&SecurityCode=1234&Amount=8.54')
        assert res.status_code == 400

    def test_invalid_cvv_alpha(self, client):
        res = client.get(
            '/payment/pay?CreditCardNumber=4111-1111-1111-1111&CardHolder=mohit&'
            'ExpirationDate=11/2/2022&SecurityCode=acs&Amount=8.54')
        assert res.status_code == 400

    def test_invalid_amount_alphanumeric(self, client):
        res = client.get(
            '/payment/pay?CreditCardNumber=4111-1111-1111-1111&CardHolder=mohit&'
            'ExpirationDate=11/2/2022&SecurityCode=123&Amount=8.54awd')
        assert res.status_code == 400

    def test_negative_amount(self, client):
        res = client.get(
            '/payment/pay?CreditCardNumber=4111-1111-1111-1111&CardHolder=mohit&'
            'ExpirationDate=27/1/2022&SecurityCode=785&Amount=-8.54')
        assert res.status_code == 400

    def test_valid_input_cheapgateway(self, client):
        res = client.get(
            '/payment/pay?CreditCardNumber=4111-1111-1111-1111&CardHolder=mohit&'
            'ExpirationDate=11/2/2022&SecurityCode=123&Amount=18.25')
        assert res.status_code == 200

    def test_valid_input_expensivegateway(self, client):
        res = client.get(
            '/payment/pay?CreditCardNumber=4111-1111-1111-1111&CardHolder=mohit&'
            'ExpirationDate=11/2/2022&SecurityCode=123&Amount=256.2')
        assert res.status_code == 200

    def test_valid_input_premiumgateway(self, client):
        res = client.get(
            '/payment/pay?CreditCardNumber=4111-1111-1111-1111&CardHolder=mohit&'
            'ExpirationDate=11/2/2022&SecurityCode=123&Amount=752.3')
        assert res.status_code == 200

    def test_valid_empty_cvv(self, client):
        res = client.get(
            '/payment/pay?CreditCardNumber=4111-1111-1111-1111&CardHolder=mohit&'
            'ExpirationDate=11/2/2022&Amount=18.25')
        assert res.status_code == 200


@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client
