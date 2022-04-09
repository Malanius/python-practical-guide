import hashlib
from typing import Callable, List

import hash_util
from block import Block
from transaction import Transaction


class Verification:
    def is_valid_proof(self, transactions: List[Transaction], last_hash: str, proof_number: int):
        guess = f'{[tx.to_ordered_dict() for tx in transactions]}{last_hash}{proof_number}'.encode()
        guess_hash = hashlib.sha256(guess).hexdigest()
        return guess_hash[0:2] == '00'

    def is_valid_chain(self, blockchain: List[Block]):
        for index, block in enumerate(blockchain):
            if index == 0:
                continue
            expected_last_hash = block.previous_hash
            actual_last_hash = hash_util.calculate_block_hash(
                blockchain[index - 1])
            if expected_last_hash != actual_last_hash:
                print(f"Previous block for block #{index} hash doesn't match!")
                print(f'Expected: {expected_last_hash}')
                print(f'Was: {actual_last_hash}')
                return False
            if not self.is_valid_proof(block.transactions[:-1], actual_last_hash, block.proof):
                print(f'Block {index} contains invalid PoW: {block}')
                return False
        return True

    def is_valid_transaction(self, transaction: Transaction, get_balance: Callable):
        sender_balance = get_balance()
        return sender_balance >= transaction.amount
