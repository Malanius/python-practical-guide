import json

DATA_FILE = 'blockchain.json'


def save_data(blockchain, open_transactions):
    with open(DATA_FILE, mode='w') as file:
        file.write(json.dumps({
            'blockchain': blockchain,
            'open_transactions': open_transactions
        }))


def load_data():
    data = {}
    with open(DATA_FILE, mode='r') as file:
        data = json.loads(file.read())
    return data
