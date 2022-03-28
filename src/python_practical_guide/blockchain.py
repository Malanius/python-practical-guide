from pytest import skip

genesis_block = {
    'previous_hash': '',
    'index': 0,
    'transactions': []
}
blockchain = [genesis_block]
open_transactions = []
owner = 'malanius'


def get_last_block_value():
    """Returns  the last block value of the current blockchain if exists, otherwise returns None"""
    if len(blockchain) < 1:
        return None
    return blockchain[-1]


def add_transaction(recepient, sender=owner, amount=1.0):
    """Appends a new value as well as the last block value to the blockchain.

    Arguments:
        :sender: The sender of the coins
        :recepient: The recepient of the coins
        :amount: The amount transfered  (default [1.0]).
    """
    transaction = {
        'sender': sender,
        'recepient': recepient,
        'amount': amount
    }
    open_transactions.append(transaction)


def mine_block():
    pass


def get_transaction_value():
    """Returns the transaction amount from user input."""
    recepient = input('Enter the recepient of the transaction: ')
    amount = float(input('Enter transaction amount: '))
    return (recepient, amount)


def get_user_choice():
    return input('Your choice: ')


def print_blocks():
    print('Blocks in chain:')
    for block in blockchain:
        print(block)
    else:
        print('-' * 20)


def change_first_block():
    if len(blockchain) > 0:
        blockchain[0] = [2]


def verify_chain():
    for index, block in enumerate(blockchain):
        if index == 0:
            continue  # there is no previous block
        if not block[0] == blockchain[index - 1]:
            return False
    return True


waiting_for_input = True
while waiting_for_input:
    print('Choose operation:')
    print('1: Add new transaction value')
    print('2: Print the blocks')
    print('h: Manipulate chain')
    print('q: Exit')
    user_choice = get_user_choice()

    if user_choice == '1':
        recepient, amount = get_transaction_value()
        add_transaction(recepient, amount=amount)
        print(open_transactions)
    elif user_choice == '2':
        print_blocks()
    elif user_choice == 'h':
        change_first_block()
    elif user_choice == 'q':
        waiting_for_input = False
    else:
        print('Invalid choice!')
    if not verify_chain():
        print('Invalid blocks in the chain!')
        break
else:
    print('User left!')

print('Done!')
