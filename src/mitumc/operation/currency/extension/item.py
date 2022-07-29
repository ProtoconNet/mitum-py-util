from ..item import CurrencyItem
from ....common import concatBytes
from ....key import Address


class CreateContractAccountsItem(CurrencyItem):
    def __init__(self, itemType, keys, amounts):
        super(CreateContractAccountsItem, self).__init__(itemType, amounts)
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


class WithdrawsItem(CurrencyItem):
    def __init__(self, itemType, target, amounts):
        super(WithdrawsItem, self).__init__(itemType, amounts)
        self.target = Address(target)

    def bytes(self):
        amounts = self.amounts

        bAmounts = bytearray()
        for amount in amounts:
            bAmounts += bytearray(amount.bytes())

        bTarget = self.target.bytes()
        bAmounts = bytes(bAmounts)

        return concatBytes(bTarget, bAmounts)

    def dict(self):
        item = {}
        item['_hint'] = self.hint.hint
        item['target'] = self.target.address

        _amounts = self.amounts
        amounts = list()
        for _amount in _amounts:
            amounts.append(_amount.dict())
        item['amounts'] = amounts

        return item;
