import functools
import hashlib
from collections import OrderedDict
from typing import List

import hash_util
import file_util

from block import Block
from transaction import Transaction

MINING_REWARD = 10

blockchain: List[Block] = []
open_transactions: List[Transaction] = []
owner = 'malanius'
participants = {'malanius'}


def get_last_block_value():
    """Returns  the last block value of the current blockchain if exists, otherwise returns None"""
    if len(blockchain) < 1:
        return None
    return blockchain[-1]


def verify_transaction(transaction: Transaction):
    sender_balance = get_balance(transaction.sender)
    return sender_balance >= transaction.amount


def add_transaction(recipient: str, sender=owner, amount=1.0):
    """Appends a new value as well as the last block value to the blockchain.

    Arguments:
        :sender: The sender of the coins
        :recipient: The recipient of the coins
        :amount: The amount transfered  (default [1.0]).
    """
    transaction = Transaction(sender, recipient, amount)
    if verify_transaction(transaction):
        open_transactions.append(transaction)
        participants.add(sender)
        participants.add(recipient)
        file_util.save_data(blockchain, open_transactions)
        return True

    return False


def get_balance(participant: str) -> float:
    tx_sender = [[tx.amount for tx in block.transactions if tx.sender == participant]
                 for block in blockchain]
    open_tx_sender = [
        tx.amount for tx in open_transactions if tx.sender == participant]
    tx_sender.append(open_tx_sender)
    amount_sent = functools.reduce(
        lambda tx_sum, tx_amt: tx_sum + sum(tx_amt) if len(tx_amt) > 0 else tx_sum, tx_sender, 0)

    tx_recipient = [[tx.amount for tx in block.transactions if tx.recipient == participant]
                    for block in blockchain]
    open_tx_recipient = [tx.amount
                         for tx in open_transactions if tx.recipient == participant]
    tx_recipient.append(open_tx_recipient)
    amount_received = functools.reduce(
        lambda tx_sum, tx_amt: tx_sum + sum(tx_amt) if len(tx_amt) > 0 else tx_sum, tx_recipient, 0)

    return amount_received - amount_sent


def is_valid_proof(transactions: List[Transaction], last_hash: str, proof_number: int):
    guess = f"{[tx.to_ordered_dict() for tx in transactions]}{last_hash}{proof_number}".encode()
    guess_hash = hashlib.sha256(guess).hexdigest()
    print(f"Guess hash: {guess_hash}")
    return guess_hash[0:2] == '00'


def pow():
    last_block = blockchain[-1]
    last_hash = hash_util.calculate_block_hash(last_block)
    proof = 0
    while not is_valid_proof(open_transactions, last_hash, proof):
        proof += 1
    return proof


def mine_block():
    last_block = blockchain[-1]
    last_block_hash = hash_util.calculate_block_hash(last_block)
    print(f"Last block hash: {last_block_hash}")
    proof = pow()
    reward_transaction = Transaction('MINING', owner, MINING_REWARD)
    copied_transactions = open_transactions[:]
    copied_transactions.append(reward_transaction)

    new_block = Block(len(blockchain), last_block_hash,
                      copied_transactions, proof)
    blockchain.append(new_block)
    print(f"Added new block to the chain: {new_block}")
    return True


def get_transaction_value():
    """Returns the transaction amount from user input."""
    recipient = input('Enter the recipient of the transaction: ')
    amount = float(input('Enter transaction amount: '))
    return (recipient, amount)


def get_user_choice():
    return input('Your choice: ')


def print_blocks():
    print('Blocks in chain:')
    for block in blockchain:
        print(block)
    else:
        print('-' * 20)


def verify_chain():
    for index, block in enumerate(blockchain):
        if index == 0:
            continue
        expected_last_hash = block.previous_hash
        actual_last_hash = hash_util.calculate_block_hash(
            blockchain[index - 1])
        if expected_last_hash != actual_last_hash:
            print(f"Previous block for block #{index} hash doesn't match!")
            print(f"Expected: {expected_last_hash}")
            print(f"Was: {actual_last_hash}")
            return False
        if not is_valid_proof(block.transactions[:-1], actual_last_hash, block.proof):
            print(f"Block contains invalid PoW: {block}")
            return False
    return True


data = file_util.load_data()
blockchain = data['blockchain']
open_transactions = data['open_transactions']
waiting_for_input = True
while waiting_for_input:
    print('Choose operation:')
    print('1: Add new transaction value')
    print('2: Mine a new block')
    print('3: Print the blocks')
    print('4: Print the participants')
    print('q: Exit')
    user_choice = get_user_choice()

    if user_choice == '1':
        recipient, amount = get_transaction_value()
        if add_transaction(recipient, amount=amount):
            print("Added transaction.")
        else:
            print("Transaction failed!")
        print(open_transactions)
    elif user_choice == '2':
        if mine_block():
            open_transactions = []
            file_util.save_data(blockchain, open_transactions)
    elif user_choice == '3':
        print_blocks()
    elif user_choice == '4':
        print(participants)
    elif user_choice == 'q':
        waiting_for_input = False
    else:
        print('Invalid choice!')
    if not verify_chain():
        print('Invalid blocks in the chain!')
        break
    print(f'Balance of {owner}: {get_balance(owner):6.2f}')
else:
    print('User left!')

print('Done!')
