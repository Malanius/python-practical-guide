# 1) Write a normal function that accepts another function as an argument. Output the result of that other function in your “normal” function.
def print_result(fn):
    print(fn(1, 2))


def sum(a, b):
    return a + b


print('Call print_result with normal function:')
print_result(sum)

# 2) Call your “normal” function by passing a lambda function – which performs any operation of your choice – as an argument.
print('Call print_result with lambda function:')
print_result(lambda a, b: a + b)


# 3) Tweak your normal function by allowing an infinite amount of arguments on which your lambda function will be executed.
def print_result_vararg(fn, *args):
    for arg in args:
        print(fn(arg[0], arg[1]))


print_result_vararg(lambda a, b: a + b, (1, 2), (3, 4), (5, 6))


# 4) Format the output of your “normal” function such that numbers look nice and are centered in a 20 character column.
def print_result_formatted(fn):
    print(f'{fn(1, 2):^20.2f}')


print_result_formatted(lambda a, b: a + b)
