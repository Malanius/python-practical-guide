import hashlib
import hashlib
import json

from block import Block


def get_hash_digest(bytes: bytes) -> str:
    return hashlib.sha256(bytes).hexdigest()


def calculate_block_hash(block: Block) -> str:
    hashable_block = block.__dict__.copy()
    hashable_block['transactions'] = [tx.to_ordered_dict()
                                      for tx in hashable_block['transactions']]
    return get_hash_digest(json.dumps(hashable_block, sort_keys=True).encode())
