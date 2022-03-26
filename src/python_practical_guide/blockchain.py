blockchain = []


def get_last_block_value():
    """Returns  the last block value of the current blockchain."""
    return blockchain[-1]


def add_value(transaction_amount, last_transaction=[1]):
    """Appends a new value as well as the last block value to the blockchain.

    Arguments:
        :transaction_amount: The amoint that should be added.
        :last_transaction: The last blockchain transaction (default [1]).
    """
    blockchain.append([last_transaction, transaction_amount])


def get_user_input():
    """Returns the transaction amount from user input."""
    return float(input('Enter transaction amount: '))


tx_amount = get_user_input()
add_value(tx_amount)

while True:
    tx_amount = get_user_input()
    add_value(tx_amount, get_last_block_value())

    print('Blocks in chain:')
    for block in blockchain:
        print(block)

print('Done!')
