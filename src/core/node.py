from crypt import methods
from flask import Flask
from flask_cors import CORS

from core.wallet import Wallet

app = Flask(__name__)
CORS(app)

wallet = Wallet()


@app.route('/', methods=['GET'])
def get_ui():
    return 'Works!'


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
