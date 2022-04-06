import json
import pickle
from collections import OrderedDict

DATA_FILE = 'blockchain.json'
DATA_FILE_PICKLE = 'blockchain.pickle'


def save_data(blockchain, open_transactions):
    with open(DATA_FILE, mode='w') as file:
        file.write(json.dumps({
            'blockchain': blockchain,
            'open_transactions': open_transactions
        }))


def save_data_pickle(blockchain, open_transactions):
    with open(DATA_FILE_PICKLE, mode='wb') as file:
        file.write(pickle.dumps({
            'blockchain': blockchain,
            'open_transactions': open_transactions
        }))


def convert_transactions(transactions):
    return [OrderedDict([('sender', tx['sender']), ('recepient', tx['recepient']), ('amount', tx['amount'])]) for tx in transactions]


def load_data():
    with open(DATA_FILE, mode='r') as file:
        file_data = json.loads(file.read())
    blockchain = [{'previous_hash': block['previous_hash'],
                   'index': block['index'],
                   'proof': block['proof'],
                   'transactions': convert_transactions(block['transactions'])
                   } for block in file_data['blockchain']]
    open_transactions = convert_transactions(file_data['open_transactions'])
    return {
        'blockchain': blockchain,
        'open_transactions': open_transactions
    }


def load_data_pickle():
    with open(DATA_FILE_PICKLE, mode='rb') as file:
        return pickle.loads(file.read())
