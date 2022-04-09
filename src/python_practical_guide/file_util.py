import json
from collections import OrderedDict
from typing import List

from block import Block

DATA_FILE = 'blockchain.json'
genesis_block = Block(0, '', [], 0, 0)


def save_data(blockchain: List[Block], open_transactions: List[OrderedDict]):
    try:
        with open(DATA_FILE, mode='w') as file:
            dumpable_chain = [block.__dict__ for block in blockchain]
            file.write(json.dumps({
                'blockchain': dumpable_chain,
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
        blockchain = [Block(block['index'], block['previous_hash'], convert_transactions(
            block['transactions']), block['proof'], block['time']) for block in file_data['blockchain']]
        open_transactions = convert_transactions(
            file_data['open_transactions'])
    except (IOError, IndexError):
        print(
            f'File {DATA_FILE} not found or empty. Initializing genesis block.')
        blockchain = [genesis_block]
    return {
        'blockchain': blockchain,
        'open_transactions': open_transactions
    }
