from collections import OrderedDict
import typing


class Transaction:
    def __init__(self, sender: str, recipient: str, amount: float) -> None:
        self.sender = sender
        self.recipient = recipient
        self.amount = amount

    def to_ordered_dict(self) -> typing.OrderedDict:
        return OrderedDict([('sender', self.sender), ('recipient', self.recipient), ('amount', self.amount)])
