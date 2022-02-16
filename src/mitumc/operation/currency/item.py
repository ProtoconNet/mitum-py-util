from ...common import _hint, concatBytes
from ...key import Address

from ...hint import (MC_CREATE_ACCOUNTS_SINGLE_AMOUNT, MC_CREATE_ACCOUNTS_MULTIPLE_AMOUNTS,
                         MC_TRANSFERS_ITEM_SINGLE_AMOUNT, MC_TRANSFERS_ITEM_MULTI_AMOUNTS)


class CreateAccountsItem(object):
    def __init__(self, keys, amounts):
        if len(amounts) > 1:
            self.hint = _hint(MC_CREATE_ACCOUNTS_MULTIPLE_AMOUNTS)
        else:
            self.hint = _hint(MC_CREATE_ACCOUNTS_SINGLE_AMOUNT)
        self.keys = keys
        self.amounts = amounts

    def bytes(self):
        amounts = self.amounts

        bAmounts = bytearray()
        for amount in amounts:
            bAmounts += bytearray(amount.bytes())

        bKeys = self.keys.bytes()
        bAmounts = bytes(bAmounts)

        return concatBytes(bKeys, bAmounts)

    def dict(self):
        item = {}
        item['_hint'] = self.hint.hint
        item['keys'] = self.keys.dict()

        _amounts = self.amounts
        amounts = list()
        for _amount in _amounts:
            amounts.append(_amount.dict())
        item['amounts'] = amounts

        return item


class TransfersItem(object):
    def __init__(self, receiver, amounts):
        if len(amounts) > 1:
            self.hint = _hint(MC_TRANSFERS_ITEM_MULTI_AMOUNTS)
        else:
            self.hint = _hint(MC_TRANSFERS_ITEM_SINGLE_AMOUNT)
        self.receiver = Address(receiver)
        self.amounts = amounts

    def bytes(self):
        amounts = self.amounts

        bAmounts = bytearray()
        for amount in amounts:
            bAmounts += bytearray(amount.bytes())

        bReceiver = self.receiver.bytes()
        bAmounts = bytes(bAmounts)

        return concatBytes(bReceiver, bAmounts)

    def dict(self):
        item = {}
        item['_hint'] = self.hint.hint
        item['receiver'] = self.receiver.address

        _amounts = list()
        for _amount in self.amounts:
            _amounts.append(_amount.dict())
        item['amounts'] = _amounts

        return item
