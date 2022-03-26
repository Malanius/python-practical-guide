blockchain = []


def get_last_block_value():
    """Returns  the last block value of the current blockchain if exists, otherwise returns None"""
    if len(blockchain) < 1:
        return None
    return blockchain[-1]


def add_transaction(transaction_amount, last_transaction):
    """Appends a new value as well as the last block value to the blockchain.

    Arguments:
        :transaction_amount: The amoint that should be added.
        :last_transaction: The last blockchain transaction (default [1]).
    """
    if last_transaction == None:
        last_transaction = [1]
    blockchain.append([last_transaction, transaction_amount])


def get_transaction_value():
    """Returns the transaction amount from user input."""
    return float(input('Enter transaction amount: '))


def get_user_choice():
    return input('Your choice: ')


def print_blocks():
    print('Blocks in chain:')
    for block in blockchain:
        print(block)


while True:
    print('Choose operation:')
    print('1: Add new transaction value')
    print('2: Print the blocks')
    print('3: Exit')
    user_choice = get_user_choice()

    if user_choice == '1':
        tx_amount = get_transaction_value()
        add_transaction(tx_amount, get_last_block_value())
    elif user_choice == '2':
        print_blocks()
    elif user_choice == '3':
        break
    else:
        print('Invalid choice!')

print('Done!')
