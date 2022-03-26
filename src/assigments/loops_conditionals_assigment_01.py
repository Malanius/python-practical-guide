# 1) Create a list of names and use a for loop to output the length of each name (len()).
names = ['Max', 'Arkoniel', 'Ichigo', 'Rukia', 'JoJo']

for name in names:
    print(f'{name} length: {len(name)}')

print('-' * 20)

# 2) Add an if check inside the loop to only output names longer than 5 characters.
print('Names longer than 5 chars:')
for name in names:
    if len(name) > 5:
        print(name)

print('-' * 20)

# 3) Add another if check to see whether a name includes a “n” or “N” character.
print('Names containing "n/N":')
for name in names:
    if 'n' in name.lower():
        print(name)

print('-' * 20)

# 4) Use a while loop to empty the list of names (via pop())
while names != []:
    name = names.pop()
    print(f'Removed {name} from list.')
else:
    print('All names removed.')
