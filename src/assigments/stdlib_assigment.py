import random
from datetime import datetime
# 1) Import the random function and generate both a random number between 0 and 1 as well as a random number between 1 and 10.
print(f"Generated number between 0-1: {random.random()}")
print(f"Generated number between 1-10: {random.randint(1,10)}")

# 2) Use the datetime library together with the random number to generate a random, unique value.
now = datetime.utcnow()
random.seed(now)
print(f"Generated value with datetime: {random.random()}")
