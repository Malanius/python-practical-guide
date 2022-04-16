from flask import Flask, jsonify
from flask_cors import CORS

from core.wallet import Wallet
from core.blockchain import Blockchain

app = Flask(__name__)
CORS(app)

wallet = Wallet()
blockchain = Blockchain(wallet.public_key)


@app.route('/', methods=['GET'])
def get_ui():
    return 'Works!'


@app.route('/chain', methods=['GET'])
def get_chain():
    chain = blockchain.chain
    dumpable_chain = [block.convert_to_dumpable_block() for block in chain]
    return jsonify(dumpable_chain), 200


@app.route('/mine', methods=['POST'])
def mine_block():
    block = blockchain.mine_block()
    if block != None:
        response = {
            'message': 'Block added sucesfully.',
            'block': block.convert_to_dumpable_block()
        }
        return jsonify(response), 201
    else:
        response = {
            'message': 'Adding block failed!',
            'wallet_set_up': wallet.public_key != None
        }
        return jsonify(response), 400


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
