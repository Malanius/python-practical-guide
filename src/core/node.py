from flask import Flask, jsonify, request
from flask_cors import CORS
from core.transaction import Transaction

from core.wallet import Wallet
from core.blockchain import Blockchain

app = Flask(__name__)
CORS(app)

wallet = Wallet()
blockchain = Blockchain(wallet.public_key)


@app.route('/', methods=['GET'])
def get_ui():
    return 'Works!'


@app.route('/wallet/create-keys', methods=['POST'])
def create_wallet():
    wallet.create_keys()
    if wallet.save_keys():
        global blockchain
        blockchain = Blockchain(wallet.public_key)
        response = {
            'public_key': wallet.public_key,
            'private_key': wallet.private_key,
        }
        return jsonify(response), 201
    else:
        response = {
            'message': 'Saving keys failed!'
        }
        return jsonify(response), 500


@app.route('/wallet/load-keys', methods=['POST'])
def load_wallet():
    if wallet.load_keys():
        global blockchain
        blockchain = Blockchain(wallet.public_key)
        return jsonify({'message': 'Keys loaded.'}), 200
    else:
        return jsonify({'message': 'Failed to load keys!'}), 500


@app.route('/wallet/balance', methods=['GET'])
def get_balance():
    balance = blockchain.get_balance()
    if balance == None:
        return jsonify({
            'message': 'No wallet set up to get balance!'
        }), 400

    return jsonify({'balance': balance}), 200


@app.route('/transactions', methods=['GET'])
def get_open_transactions():
    transactions = blockchain.get_open_transactions()
    dumpable_transactions = [tx.to_ordered_dict() for tx in transactions]
    return jsonify(dumpable_transactions), 200


@app.route('/transactions', methods=['POST'])
def add_transaction():
    if wallet.public_key == None:
        return jsonify({'message': 'No wallet set up!'}), 400

    request_data = request.get_json()
    if not request_data:
        print('No request body!')
        return jsonify({'message': 'No data!'}), 400

    required_fileds = ['recipient', 'amount']
    if not all(field in request_data for field in required_fileds):
        return jsonify({'message': 'Missing required data!'}), 400

    recipient = request_data['recipient']
    amount = request_data['amount']
    signature = wallet.sign_transaction(wallet.public_key, recipient, amount)
    new_transaction = blockchain.add_transaction(
        recipient, wallet.public_key, signature, amount)

    if new_transaction == None:
        return jsonify({'message': 'Adding transaction failed!'}), 400

    return jsonify({'message': 'Transaction sucessful.',
                    'transaction': new_transaction.to_ordered_dict()}), 201


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
