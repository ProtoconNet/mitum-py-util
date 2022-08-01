from .base import Amount
from .item import CreateAccountsItem, TransfersItem
from .fact import CreateAccountsFact, KeyUpdaterFact, TransfersFact
from .extension import CurrencyExtensionGenerator

from ..base import OperationGenerator
from ...hint import (
    MC_CREATE_ACCOUNTS_MULTIPLE_AMOUNTS, MC_CREATE_ACCOUNTS_SINGLE_AMOUNT, 
    MC_TRANSFERS_ITEM_MULTI_AMOUNTS, MC_TRANSFERS_ITEM_SINGLE_AMOUNT
)
from ...key import Key, Keys


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
        self.extension = CurrencyExtensionGenerator(id)

    def setId(self, id):
        super(CurrencyGenerator, self).setId(id)
        self.extension = CurrencyExtensionGenerator(id)

    def key(self, key, weight):
        return (key, weight)

    def amount(self, cid, big):
        return (cid, big)

    def keys(self, keys, threshold):
        return _to_keys(keys, threshold)

    def amounts(self, amounts):
        return _to_amounts(amounts)

    def getCreateAccountsItem(self, keys, amounts):
        if len(amounts) > 1:
            return CreateAccountsItem(MC_CREATE_ACCOUNTS_MULTIPLE_AMOUNTS, keys, amounts)
        else:
            return CreateAccountsItem(MC_CREATE_ACCOUNTS_SINGLE_AMOUNT, keys, amounts)

    def getTransfersItem(self, receiver, amounts):
        if len(amounts) > 1:
            return TransfersItem(MC_TRANSFERS_ITEM_MULTI_AMOUNTS, receiver, amounts)
        else:
            return TransfersItem(MC_TRANSFERS_ITEM_SINGLE_AMOUNT, receiver, amounts)

    def getCreateAccountsFact(self, sender, items):
        return CreateAccountsFact(sender, items)

    def getKeyUpdaterFact(self, target, keys, cid):
        return KeyUpdaterFact(target, keys, cid)

    def getTransfersFact(self, sender, items):
        return TransfersFact(sender, items)
