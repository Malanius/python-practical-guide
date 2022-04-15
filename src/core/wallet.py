import binascii

import Crypto.Random
from Crypto.PublicKey import RSA
from Crypto.Signature import pkcs1_15
from Crypto.Hash import SHA256

KEY_FILE = 'wallet.keys'


class Wallet:
    def __init__(self) -> None:
        self.private_key = None
        self.public_key = None

    def create_keys(self) -> None:
        private_key, public_key = self.generate_keys()
        self.private_key = private_key
        self.public_key = public_key
        self.save_keys()

    def save_keys(self):
        try:
            with open(KEY_FILE, 'w') as key_file:
                key_file.write(self.public_key)
                key_file.write('\n')
                key_file.write(self.private_key)
        except (IOError, IndexError):
            print('Failed to save keys to file!')

    def load_keys(self):
        try:
            with open(KEY_FILE, 'r') as key_file:
                keys = key_file.readlines()
                print(f'---> {keys} <---')
                self.public_key = keys[0][:-1]
                self.private_key = keys[1]
        except (IOError, IndexError):
            print('Failed to load keys from file!')

    def generate_keys(self):
        private_key = RSA.generate(2048, Crypto.Random.new().read)
        public_key = private_key.publickey()
        return (binascii.hexlify(private_key.exportKey(format='DER')).decode('ascii'),
                binascii.hexlify(public_key.exportKey(format='DER')).decode('ascii'))

    def sign_transaction(self, sender, recipient, amount):
        signer_identity = pkcs1_15.new(RSA.import_key(
            binascii.unhexlify(self.private_key)))
        transaction_hash = SHA256.new(
            (f"{sender}{recipient}{amount}").encode('utf8'))
        signature = signer_identity.sign(transaction_hash)
        return binascii.hexlify(signature).decode('ascii')
