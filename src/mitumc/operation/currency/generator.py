from mitumc.key import Key, Keys

from mitumc.operation.base import OperationGenerator
from mitumc.operation.currency.base import Amount
from mitumc.operation.currency.item import CreateAccountsItem, TransfersItem
from mitumc.operation.currency.fact import CreateAccountsFact, KeyUpdaterFact, TransfersFact


def _to_keys(keys, threshold):
    _keys = []

    for _key in keys:
        key, weight = _key

        _keys.append(
            Key(key, weight)
        )

    return Keys(
        _keys,
        threshold,
    )


def _to_amounts(amounts):
    _amounts = []

    for _amt in amounts:
        _amounts.append(
            Amount(
                _amt[0],
                _amt[1]
            )
        )

    return _amounts


class CurrencyGenerator(OperationGenerator):
    def __init__(self, id):
        super(CurrencyGenerator, self).__init__(id)

    def key(self, key, weight):
        return (key, weight)

    def amount(self, big, cid):
        return (big, cid)

    def createKeys(self, keys, threshold):
        return _to_keys(keys, threshold)

    def createAmounts(self, amounts):
        return _to_amounts(amounts)

    def createCreateAccountsItem(self, keys, amounts):
        return CreateAccountsItem(keys, amounts)

    def createTransfersItem(self, receiver, amounts):
        return TransfersItem(receiver, amounts)

    def createCreateAccountsFact(self, sender, items):
        return CreateAccountsFact(sender, items)

    def createKeyUpdaterFact(self, target, keys, cid):
        return KeyUpdaterFact(target, keys, cid)

    def createTransfersFact(self, sender, items):
        return TransfersFact(sender, items)
