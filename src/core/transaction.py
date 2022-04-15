from collections import OrderedDict
from inspect import signature
import typing

from util.printable import Printable


class Transaction(Printable):
    def __init__(self, sender: str, recipient: str, signature: str, amount: float) -> None:
        self.sender = sender
        self.recipient = recipient
        self.signature = signature
        self.amount = amount

    def to_ordered_dict(self) -> typing.OrderedDict:
        return OrderedDict([('sender', self.sender), ('recipient', self.recipient), ('signature', self.signature), ('amount', self.amount)])
