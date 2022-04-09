import json
from collections import OrderedDict
from typing import List, TypedDict

from block import Block
from transaction import Transaction

DATA_FILE = 'blockchain.json'
genesis_block = Block(0, '', [], 0, 0)


def convert_to_dumpable_block(block: Block) -> dict:
    dumpable_block = block.__dict__.copy()
    dumpable_block['transactions'] = [tx.to_ordered_dict()
                                      for tx in dumpable_block['transactions']]
    return dumpable_block


def save_data(blockchain: List[Block], open_transactions: List[Transaction]):
    try:
        with open(DATA_FILE, mode='w') as file:
            dumpable_chain = [convert_to_dumpable_block(
                block) for block in blockchain]
            dumpable_transactions = [
                transaction.__dict__ for transaction in open_transactions]
            file.write(json.dumps({
                'blockchain': dumpable_chain,
                'open_transactions': dumpable_transactions
            }))
    except IOError:
        print('Saving data failed!')


def convert_transactions(transactions) -> List[Transaction]:
    return [Transaction(tx['sender'], tx['recipient'], tx['amount']) for tx in transactions]


class ChainData(TypedDict):
    blockchain: List[Block]
    open_transactions: List[Transaction]


def load_data() -> ChainData:
    blockchain = []
    open_transactions = []
    try:
        with open(DATA_FILE, mode='r') as file:
            file_data = json.loads(file.read())
        blockchain = [Block(block['index'], block['previous_hash'], convert_transactions(
            block['transactions']), block['proof'], block['timestamp']) for block in file_data['blockchain']]
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
