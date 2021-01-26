from flask import Blueprint, request
from werkzeug.exceptions import abort
from decimal import Decimal
from external_services.gateway_payment import externalServices
import regex as re
import datetime

processpayment = Blueprint("processpayment", __name__)

@processpayment.route("/pay")
def ProcessPayment():
    params = {"CreditCardNumber": request.args.get('CreditCardNumber'),
              "CardHolder": request.args.get('CardHolder'),
              "ExpirationDate": request.args.get('ExpirationDate'),
              "SecurityCode": request.args.get('SecurityCode', None),
              "Amount": request.args.get('Amount')}
    if not validate_paramters(params):
        abort(400)
    try:
        gateway = externalServices(params)
        status = gateway.make_payment()
        if status:
            return {"status": 'Payment is processed'}, 200
        else:
            abort(400)
    except:
        abort(500)
    print(params)
    # return 'Payment is processed', 200

def card_validator(number):
    # pattern to match VISA/MasterCard only with 16 digits
    pattern = r'^((4\d{3})|(5[1-5]\d{2}))-?\d{4}-?\d{4}-?\d{4}$'
    if not re.search(pattern, number):
        return False
    return True

def verify_amount(amount):
    try:
        if not Decimal(amount) > 0:
            return False
        return True
    except:
        return False

def validate_paramters(params):
    # params['CreditCardNumber'] = params['CreditCardNumber']
    # print(datetime.datetime.strptime(params['ExpirationDate'], "%d/%m/%Y"))
    # print(Decimal(params['Amount']))
    if not type(params['CreditCardNumber']) == str or not len(params['CreditCardNumber'].replace("-","").strip()) == 16:
        return False
    if not card_validator(params['CreditCardNumber'].strip()):
        return False
    if not type(params['CardHolder']) == str or not params['CardHolder']:
        return False
    if not datetime.datetime.strptime(params['ExpirationDate'], "%d/%m/%Y") > datetime.datetime.now():
        return False
    if params['SecurityCode']:
        if not (type(params['SecurityCode']) == str and len(params['SecurityCode']) == 3) or not params['SecurityCode'].isdigit():
            return False
    if not verify_amount(params['Amount']):
        return False
    return True