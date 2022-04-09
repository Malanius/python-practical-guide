# 1) Create a Food class with a “name” and a “kind” attribute as well as a “describe()” method (which prints “name” and “kind” in a sentence).
# 2) Try turning describe() from an instance method into a class and a static method. Change it back to an instance method thereafter.
# 3) Create a  “Meat” and a “Fruit” class – both should inherit from “Food”. Add a “cook()” method to “Meat” and “clean()” to “Fruit”.
# 4) Overwrite a “dunder” method to be able to print your “Food” class.

class Food:
    def __init__(self, name: str, kind: str) -> None:
        self.name = name
        self.kind = kind

    def __repr__(self) -> str:
        return str(self.__dict__)

    def describe(self):
        print(f'{self.name} is kind of {self.kind}')


apple = Food('apple', 'fruit')
apple.describe()
print('-'*20)


class Meat(Food):
    def __init__(self, name: str) -> None:
        super().__init__(name, 'meat')

    def cook(self):
        print(f'Coocking {self.name} {self.kind}...')


beef = Meat('beef')
beef.describe()
beef.cook()
print('-'*20)


class Fruit(Food):
    def __init__(self, name: str) -> None:
        super().__init__(name, 'fruit')

    def clean(self):
        print(f'Cleaning {self.name}...')


apple = Fruit('apple')
apple.describe()
apple.clean()
print('-'*20)

print(beef)
print(apple)
