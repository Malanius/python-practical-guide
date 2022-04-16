import binascii

import Crypto.Random
from Crypto.PublicKey import RSA
from Crypto.Signature import pkcs1_15
from Crypto.Hash import SHA256

from core.transaction import Transaction

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
                return True
        except (IOError, IndexError):
            print('Failed to save keys to file!')
            return False

    def load_keys(self):
        try:
            with open(KEY_FILE, 'r') as key_file:
                keys = key_file.readlines()
                print(f'---> {keys} <---')
                self.public_key = keys[0][:-1]
                self.private_key = keys[1]
                return True
        except (IOError, IndexError):
            print('Failed to load keys from file!')
            return False

    def generate_keys(self):
        private_key = RSA.generate(2048, Crypto.Random.new().read)
        public_key = private_key.publickey()
        return (binascii.hexlify(private_key.exportKey(format='DER')).decode('ascii'),
                binascii.hexlify(public_key.exportKey(format='DER')).decode('ascii'))

    def sign_transaction(self, sender: str, recipient: str, amount: float):
        signer_identity = pkcs1_15.new(RSA.import_key(
            binascii.unhexlify(self.private_key)))
        transaction_hash = SHA256.new(
            (f"{sender}{recipient}{amount}").encode('utf8'))
        signature = signer_identity.sign(transaction_hash)
        return binascii.hexlify(signature).decode('ascii')

    @staticmethod
    def verify_transaction(transaction: Transaction):
        public_key = RSA.import_key(binascii.unhexlify(transaction.sender))
        verifier = pkcs1_15.new(public_key)
        transaction_hash = SHA256.new(
            (f"{transaction.sender}{transaction.recipient}{transaction.amount}").encode('utf8'))
        try:
            verifier.verify(transaction_hash,
                            binascii.unhexlify(transaction.signature))
            return True
        except ValueError:
            print('Invalid signature detected!')
            return False
