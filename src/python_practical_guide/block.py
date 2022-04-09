from time import time


class Block:
    def __init__(self, index: int, previous_hash: str, transactions: list, proof: int, timestamp=None) -> None:
        self.index = index
        self.previous_hash = previous_hash
        self.timestamp = time() if timestamp is None else timestamp
        self.transactions = transactions
        self.proof = proof
