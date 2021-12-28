import base64

from mitumc.common import bconcat, _hint
from mitumc.hash import sha3
from mitumc.hint import MC_CREATE_ACCOUNTS_MULTIPLE_AMOUNTS, MC_CREATE_ACCOUNTS_OP_FACT, MC_CREATE_ACCOUNTS_SINGLE_AMOUNT
from mitumc.operation.base import OperationFact, Address


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

        bamounts = bytearray()
        for amount in amounts:
            bamounts += bytearray(amount.bytes())

        bkeys = self.keys.bytes()
        bamounts = bytes(bamounts)

        return bconcat(bkeys, bamounts)

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


class CreateAccountsFact(OperationFact):
    def __init__(self, sender, items):
        super(CreateAccountsFact, self).__init__(MC_CREATE_ACCOUNTS_OP_FACT)
        self.sender = Address(sender)
        self.items = items
        self.hash = sha3(self.bytes())

    def bytes(self):
        bitems = bytearray()
        for i in self.items:
            bitems += bytearray(i.bytes())
        
        btoken = self.token.encode()
        bsender = self.sender.bytes()
        bitems = bytes(bitems)

        return bconcat(btoken, bsender, bitems)

    def dict(self):
        fact = {}
        fact['_hint'] = self.hint.hint
        fact['hash'] = self.hash.hash
        token = base64.b64encode(self.token.encode('ascii')).decode('ascii')
        fact['token'] = token
        fact['sender'] = self.sender.address

        _items = list()
        for item in self.items:
            _items.append(item.dict())
        fact['items'] = _items
        return fact