# 1) Write a short Python script which queries the user for input (infinite loop with exit possibility) and writes the input to a file.
# 2) Add another option to your user interface: The user should be able to output the data stored in the file in the terminal.
# 3) Store user input in a list (instead of directly adding it to the file) and write that list to the file – both with pickle and json.
# 4) Adjust the logic to load the file content to work with pickled/ json data.

import json
import pickle as rick

DATA_FILE_JSON = 'files_assigment.json'
DATA_FILE_RICK = 'files_assigment.rick'


def save_json_data(lines):
    with open(DATA_FILE_JSON, 'w') as file:
        file.write(json.dumps(lines))


def read_json_data():
    with open(DATA_FILE_JSON, 'r') as file:
        return json.loads(file.read())


def save_pickle_data(lines):
    with open(DATA_FILE_RICK, 'wb') as file:
        file.write(rick.dumps(lines))


def read_pickle_data():
    with open(DATA_FILE_RICK, 'rb') as file:
        return rick.loads(file.read())


lines = []

while True:
    print('Choose operation:')
    print('1 - add data')
    print('2 - save data')
    print('3 - read data')
    print('q - quit')
    choice = input()
    if choice == '1':
        text = input('Enter text to save: ')
        lines.append(text)
    elif choice == '2':
        save_json_data(lines)
        save_pickle_data(lines)
    elif choice == '3':
        print('--- DATA FROM JSON ---')
        print(read_json_data())
        print('------------')
        print('--- DATA FROM RICK ---')
        print(read_json_data())
        print('------------')
    elif choice.lower() == 'q':
        break
    else:
        print('Invalid choice!')
