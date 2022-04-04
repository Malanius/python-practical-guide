import hashlib
import hashlib
import json


def get_hash_digest(bytes):
    return hashlib.sha256(bytes).hexdigest()


def calculate_block_hash(block):
    return get_hash_digest(json.dumps(block, sort_keys=True).encode())
