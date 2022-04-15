from time import time
from typing import List

from util.printable import Printable
from transaction import Transaction


class Block(Printable):
    def __init__(self, index: int, previous_hash: str, transactions: List[Transaction], proof: int, timestamp=None) -> None:
        self.index = index
        self.previous_hash = previous_hash
        self.timestamp = time() if timestamp is None else timestamp
        self.transactions = transactions
        self.proof = proof

    def convert_to_dumpable_block(self) -> dict:
        dumpable = self.__dict__.copy()
        dumpable['transactions'] = [tx.to_ordered_dict()
                                    for tx in dumpable['transactions']]
        return dumpable
