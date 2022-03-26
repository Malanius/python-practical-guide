# 1 Create two variables – one with your name and one with your age

name = 'Someone'
age = 69

# 2 Create a function which prints your data as one string


def print_name_and_age():
    print(f'{name}: {age}')


print_name_and_age()

# 3 Create a function which prints ANY data (two arguments) as one string


def print_two_args_as_string(arg1, arg2):
    print(f'{arg1} {arg2}')


print_two_args_as_string('completed:', True)

# 4 Create a function which calculates and returns the number of decades you already lived (e.g. 23 = 2 decades)


def calculate_endured_decades(age):
    return age // 10


print(calculate_endured_decades(69))
