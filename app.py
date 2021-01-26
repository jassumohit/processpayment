from flask import Flask, jsonify
from processpayment import processpayment

app = Flask(__name__)


@app.errorhandler(500)
def internal_error(error):
    return jsonify(error="internal server error"), 500


@app.errorhandler(Exception)
def not_found(error):
    return jsonify(error="The request is invalid"), 400


app.register_blueprint(processpayment, url_prefix='/payment')


@app.route("/health")
def home():
    return jsonify(status="Success"), 200


if __name__ == "__main__":
    app.run()
