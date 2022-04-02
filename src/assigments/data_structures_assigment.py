from copy import deepcopy

# 1) Create a list of “person” dictionaries with a name, age and list of hobbies for each person. Fill in any data you want.
persons = [
    {'name': 'malanius', 'age': 99, 'hobbies': ['code', 'games']},
    {'name': 'arkoniel', 'age': 179, 'hobbies': ['magic', 'books']},
    {'name': 'larien', 'age': 26, 'hobbies': ['treasure hunting']},
]

# 2) Use a list comprehension to convert this list of persons into a list of names (of the persons).
names = [person['name'] for person in persons]
print(f"Names: {names}")

# 3) Use a list comprehension to check whether all persons are older than 20.
older_than_20 = all([person['age'] > 20 for person in persons])
print(f"All older than 20: {older_than_20}")

# 4) Copy the person list such that you can safely edit the name of the first person (without changing the original list).
# copied_persons = persons[:] - won't work as this creates shallow copy, so modyfing any name in copied list also changes the original one
# copied_persons = persons[:]
copied_persons = deepcopy(persons)
copied_persons[0]['name'] = 'mal'
print(f"Original: {persons}")
print(f"New: {copied_persons}")

# 5) Unpack the persons of the original list into different variables and output these variables.
mal, ark, lar = persons
print("All unpaccked:")
print(mal)
print(ark)
print(lar)

mal, *rest = persons
print("Unpacked first and rest:")
print(mal)
print(rest)

*rest, lar = persons
print("Unpacked rest and last:")
print(rest)
print(lar)

mal, *rest, lar = persons
print("Unpacked first,rest and last:")
print(mal)
print(rest)
print(lar)

