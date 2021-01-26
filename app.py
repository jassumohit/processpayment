from flask import Flask, jsonify
from werkzeug.exceptions import HTTPException
from processpayment import processpayment

app = Flask(__name__)


@app.errorhandler(500)
def internal_error(error):
    return jsonify(error="internal server error"), 500


@app.errorhandler(Exception)
def not_found(error):
    return jsonify(error="The request is invalid"), error.code


# @app.errorhandler(Exception)
# def global_exception(e):
#     if isinstance(e, HTTPException):
#         return jsonify(error="The request is invalid"), e.code
#     else:
#         return jsonify(error="internal server error"), 500

app.register_blueprint(processpayment, url_prefix='/payment')


@app.route("/home")
def home():
    return "Hola it worked"


if __name__ == "__main__":
    app.run()
