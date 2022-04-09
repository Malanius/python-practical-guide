import json
from collections import OrderedDict

DATA_FILE = 'blockchain.json'

genesis_block = {
    'previous_hash': '',
    'index': 0,
    'transactions': [],
    'proof': 0
}


def save_data(blockchain, open_transactions):
    try:
        with open(DATA_FILE, mode='w') as file:
            file.write(json.dumps({
                'blockchain': blockchain,
                'open_transactions': open_transactions
            }))
    except IOError:
        print('Saving data failed!')


def convert_transactions(transactions):
    return [OrderedDict([('sender', tx['sender']), ('recepient', tx['recepient']), ('amount', tx['amount'])]) for tx in transactions]


def load_data():
    blockchain = []
    open_transactions = []
    try:
        with open(DATA_FILE, mode='r') as file:
            file_data = json.loads(file.read())
        blockchain = [{'previous_hash': block['previous_hash'],
                       'index': block['index'],
                       'proof': block['proof'],
                       'transactions': convert_transactions(block['transactions'])
                       } for block in file_data['blockchain']]
        open_transactions = convert_transactions(
            file_data['open_transactions'])
    except IOError:
        print(f'File {DATA_FILE} not found. Initializing genesis block.')
        blockchain = [genesis_block]
    return {
        'blockchain': blockchain,
        'open_transactions': open_transactions
    }
