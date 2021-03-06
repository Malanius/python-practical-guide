from typing import Iterable

from core.blockchain import Blockchain
from core.wallet import Wallet
from util.verification import Verification


class Node:

    def __init__(self):
        self.wallet = Wallet()
        self.blockchain = None

    def get_transaction_value(self):
        """Returns the transaction amount from user input."""
        recipient = input('Enter the recipient of the transaction: ')
        amount = float(input('Enter transaction amount: '))
        return (recipient, amount)

    def get_user_choice(self):
        return input('Your choice: ')

    def print_iterable(self, iterable: Iterable, message: str):
        print(message)
        print('-' * 20)
        for item in iterable:
            print(item)
        else:
            print('-' * 20)

    def listen_for_input(self):
        waiting_for_input = True
        while waiting_for_input:
            print('Choose operation:')
            print('1: Add new transaction value')
            print('2: Mine a new block')
            print('3: Print the blocks')
            print('4: Print open transactions')
            print('5: Validate open transactions')
            print('6: Create wallet')
            print('7: Load wallet')
            print('q: Exit')
            user_choice = self.get_user_choice()

            if user_choice == '1':
                recipient, amount = self.get_transaction_value()
                signature = self.wallet.sign_transaction(self.wallet.public_key, recipient, amount)
                if self.blockchain.add_transaction(recipient, self.wallet.public_key, signature, amount):
                    print('Transaction sucessful.')
                else:
                    print('Transaction failed!')
            elif user_choice == '2':
                if self.blockchain == None:
                    print('Mining failed. Got no wallet?')
                else:
                    self.blockchain.mine_block()
            elif user_choice == '3':
                self.print_iterable(self.blockchain.chain, 'Blocks in chain:')
            elif user_choice == '4':
                self.print_iterable(
                    self.blockchain.get_open_transactions(), 'Open transactions:')
            elif user_choice == '5':
                if Verification.verify_transactions(self.blockchain.get_open_transactions(), self.blockchain.get_balance):
                    print('All open transactions are valid.')
                else:
                    print('There are invalid transactions!')
            elif user_choice == '6':
                self.wallet.create_keys()
                self.blockchain = Blockchain(self.wallet.public_key)
            elif user_choice == '7':
                self.wallet.load_keys()
                self.blockchain = Blockchain(self.wallet.public_key)
            elif user_choice == 'q':
                waiting_for_input = False
            else:
                print('Invalid choice!')
            if self.blockchain != None:
                if not Verification.is_valid_chain(self.blockchain.chain):
                    print('Invalid blocks in the chain!')
                    break
                print(
                    f'Balance of {self.wallet.public_key}: {self.blockchain.get_balance():6.2f}')
        else:
            print('User left.')

        print('Bye!')


if __name__ == '__main__':
    node = Node()
    node.listen_for_input()
