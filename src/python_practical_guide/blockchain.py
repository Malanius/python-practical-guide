blockchain = [[1]]


def get_last_block_value():
    return blockchain[-1]


def add_value(transaction_amount):
    blockchain.append([get_last_block_value(), transaction_amount])


add_value(2)
add_value(0.9)
add_value(10.89)

print(blockchain)
