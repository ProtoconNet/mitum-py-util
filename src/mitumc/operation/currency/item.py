from ..base import Item
from ...common import _hint, concatBytes
from ...key import Address
from ...hint import MC_TRANSFERS_ITEM_SINGLE_AMOUNT, MC_TRANSFERS_ITEM_MULTI_AMOUNTS


class CurrencyItem(Item):
    def __init__(self, itemType, amounts):
        super(CurrencyItem, self).__init__(itemType)
        self.amounts = amounts


class CreateAccountsItem(CurrencyItem):
    def __init__(self, itemType, keys, amounts):
        super(CreateAccountsItem, self).__init__(itemType, amounts)
        self.keys = keys

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


class TransfersItem(CurrencyItem):
    def __init__(self, itemType, receiver, amounts):
        super(TransfersItem, self).__init__(itemType, amounts)
        self.receiver = Address(receiver)

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
