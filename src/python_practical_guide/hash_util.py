import hashlib
import hashlib
import json

from block import Block


def get_hash_digest(bytes: bytes) -> str:
    return hashlib.sha256(bytes).hexdigest()


def calculate_block_hash(block: Block) -> str:
    # copy so we don't change references of each previously hashed block
    hashable_block = block.__dict__.copy()
    return get_hash_digest(json.dumps(hashable_block, sort_keys=True).encode())
