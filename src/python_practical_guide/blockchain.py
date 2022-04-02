genesis_block = {
    'previous_hash': '',
    'index': 0,
    'transactions': []
}
blockchain = [genesis_block]
open_transactions = []
owner = 'malanius'
participants = {'malanius'}


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
    participants.add(sender)
    participants.add(recepient)


def get_balance(participant):
    # TODO: make this work for more than one icoming/outgoing transaction to participant in the block
    tx_sender = [[tx['amount'] for tx in block['transactions'] if tx['sender'] == participant]
                 for block in blockchain]
    amount_sent = 0
    for tx in tx_sender:
        if len(tx) > 0:
            amount_sent += tx[0]

    tx_recepient = [[tx['amount'] for tx in block['transactions'] if tx['recepient'] == participant]
                    for block in blockchain]
    amount_received = 0
    for tx in tx_recepient:
        if len(tx) > 0:
            amount_received += tx[0]

    return amount_received - amount_sent


def calculate_block_hash(block):
    return '-'.join([str(value) for value in block.values()])


def mine_block():
    last_block = blockchain[-1]
    # temp hash using all block values
    last_block_hash = calculate_block_hash(last_block)
    print(f"Last block hash: {last_block_hash}")

    new_block = {
        'previous_hash': last_block_hash,
        'index': len(blockchain),
        'transactions': open_transactions
    }
    blockchain.append(new_block)
    print(f"Added new block to the chain: {new_block}")
    return True


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
        blockchain[0] = {
            'previous_hash': '',
            'index': 0,
            'transactions': [{'sender': 'hack',  'recepient': 'hack', 'amount': 1_000.0}]
        }


def verify_chain():
    for index, block in enumerate(blockchain):
        if index == 0:
            continue
        expected_last_hash = block['previous_hash']
        actual_last_hash = calculate_block_hash(blockchain[index - 1])
        if expected_last_hash != actual_last_hash:
            print(f"Previous block for block #{index} hash doesn't match!")
            print(f"Expected: {expected_last_hash}")
            print(f"Was: {actual_last_hash}")
            return False
    return True


waiting_for_input = True
while waiting_for_input:
    print('Choose operation:')
    print('1: Add new transaction value')
    print('2: Mine a new block')
    print('3: Print the blocks')
    print('4: Print the participants')
    print('h: Manipulate chain')
    print('q: Exit')
    user_choice = get_user_choice()

    if user_choice == '1':
        recepient, amount = get_transaction_value()
        add_transaction(recepient, amount=amount)
        print(open_transactions)
    elif user_choice == '2':
        if mine_block():
            open_transactions = []
    elif user_choice == '3':
        print_blocks()
    elif user_choice == '4':
        print(participants)
    elif user_choice == 'h':
        change_first_block()
    elif user_choice == 'q':
        waiting_for_input = False
    else:
        print('Invalid choice!')
    if not verify_chain():
        print('Invalid blocks in the chain!')
        break
    print(get_balance(owner))
else:
    print('User left!')

print('Done!')
