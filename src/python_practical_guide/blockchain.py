import functools
import json
from typing import List, TypedDict

import hash_util
from block import Block
from verification import Verification
from transaction import Transaction

MINING_REWARD = 10
DATA_FILE = 'blockchain.json'
genesis_block = Block(0, '', [], 0, 0)


class Blockchain:
    def __init__(self, hosting_node) -> None:
        self.chain: List[Block] = [genesis_block]
        self.open_transactions: List[Transaction] = []
        self.hosting_node = hosting_node
        self.load_data()

    def convert_transactions(self, transactions) -> List[Transaction]:
        return [Transaction(tx['sender'], tx['recipient'], tx['amount']) for tx in transactions]

    def load_data(self) -> None:
        try:
            with open(DATA_FILE, mode='r') as file:
                file_data = json.loads(file.read())
            blockchain = [Block(block['index'], block['previous_hash'], self.convert_transactions(
                block['transactions']), block['proof'], block['timestamp']) for block in file_data['blockchain']]
            open_transactions = self.convert_transactions(
                file_data['open_transactions'])
            self.chain = blockchain
            self.open_transactions = open_transactions
        except (IOError, IndexError):
            print(f'File {DATA_FILE} not found or empty!')

    def save_data(self) -> None:
        try:
            with open(DATA_FILE, mode='w') as file:
                dumpable_chain = [block.convert_to_dumpable_block()
                                  for block in self.chain]
                dumpable_transactions = [
                    transaction.__dict__ for transaction in self.open_transactions]
                file.write(json.dumps({
                    'blockchain': dumpable_chain,
                    'open_transactions': dumpable_transactions
                }))
        except IOError:
            print('Saving data failed!')

    def get_last_block_value(self) -> Block:
        """Returns  the last block value of the current blockchain if exists, otherwise returns None"""
        if len(self.chain) < 1:
            return None
        return self.chain[-1]

    def add_transaction(self, recipient: str, sender, amount=1.0) -> bool:
        """Appends a new value as well as the last block value to the blockchain.

        Arguments:
            :sender: The sender of the coins
            :recipient: The recipient of the coins
            :amount: The amount transfered  (default [1.0]).
        """
        transaction = Transaction(sender, recipient, amount)
        if Verification.is_valid_transaction(transaction, self.get_balance):
            self.open_transactions.append(transaction)
            self.save_data()
            print(f'Added transaction: {transaction}')
            return True

        return False

    def get_balance(self) -> float:
        participant = self.hosting_node
        tx_sender = [[tx.amount for tx in block.transactions if tx.sender == participant]
                     for block in self.chain]
        open_tx_sender = [
            tx.amount for tx in self.open_transactions if tx.sender == participant]
        tx_sender.append(open_tx_sender)
        amount_sent = functools.reduce(
            lambda tx_sum, tx_amt: tx_sum + sum(tx_amt) if len(tx_amt) > 0 else tx_sum, tx_sender, 0)

        tx_recipient = [[tx.amount for tx in block.transactions if tx.recipient == participant]
                        for block in self.chain]
        open_tx_recipient = [tx.amount
                             for tx in self.open_transactions if tx.recipient == participant]
        tx_recipient.append(open_tx_recipient)
        amount_received = functools.reduce(
            lambda tx_sum, tx_amt: tx_sum + sum(tx_amt) if len(tx_amt) > 0 else tx_sum, tx_recipient, 0)

        return amount_received - amount_sent

    def pow(self) -> int:
        last_block = self.chain[-1]
        last_hash = hash_util.calculate_block_hash(last_block)
        proof = 0
        while not Verification.is_valid_proof(self.open_transactions, last_hash, proof):
            proof += 1
        return proof

    def mine_block(self) -> None:
        last_block = self.chain[-1]
        last_block_hash = hash_util.calculate_block_hash(last_block)
        proof = self.pow()
        reward_transaction = Transaction(
            'MINING', self.hosting_node, MINING_REWARD)
        copied_transactions = self.open_transactions[:]
        copied_transactions.append(reward_transaction)

        new_block = Block(len(self.chain), last_block_hash,
                          copied_transactions, proof)
        self.chain.append(new_block)
        print(f'Added new block to the chain: {new_block}')
        self.open_transactions = []
        self.save_data()
