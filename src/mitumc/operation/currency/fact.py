import base64

from mitumc.hash import sha3
from mitumc.common import concatBytes
from mitumc.key import Address

from mitumc.hint import MC_CREATE_ACCOUNTS_OP_FACT, MC_KEYUPDATER_OP_FACT, MC_TRANSFERS_OP_FACT
from mitumc.operation.base import OperationFact


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

        bToken = self.token.encode()
        bSender = self.sender.bytes()
        bitems = bytes(bitems)

        return concatBytes(bToken, bSender, bitems)

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


class KeyUpdaterFact(OperationFact):
    def __init__(self, target, keys, cid):
        super(KeyUpdaterFact, self).__init__(MC_KEYUPDATER_OP_FACT)
        self.target = Address(target)
        self.cid = cid
        self.keys = keys
        self.hash = sha3(self.bytes())

    def bytes(self):
        bToken = self.token.encode()
        bTarget = self.target.bytes()
        bKeys = self.keys.bytes()
        bCid = self.cid.encode()

        return concatBytes(bToken, bTarget, bKeys, bCid)

    def dict(self):
        fact = {}
        fact['_hint'] = self.hint.hint
        fact['hash'] = self.hash.hash
        fact['token'] = base64.b64encode(
            self.token.encode('ascii')).decode('ascii')
        fact['target'] = self.target.address
        fact['keys'] = self.keys.dict()
        fact['currency'] = self.cid
        return fact


class TransfersFact(OperationFact):
    def __init__(self, sender, items):
        super(TransfersFact, self).__init__(MC_TRANSFERS_OP_FACT)
        self.sender = Address(sender)
        self.items = items
        self.hash = sha3(self.bytes())

    def bytes(self):
        bitems = bytearray()
        for i in self.items:
            bitems += bytearray(i.bytes())

        bToken = self.token.encode()
        bSender = self.sender.bytes()
        bitems = bytes(bitems)

        return concatBytes(bToken, bSender, bitems)

    def dict(self):
        fact = {}
        fact['_hint'] = self.hint.hint
        fact['hash'] = self.hash.hash
        fact['token'] = base64.b64encode(
            self.token.encode('ascii')).decode('ascii')
        fact['sender'] = self.sender.address

        _items = list()
        for _item in self.items:
            _items.append(_item.dict())
        fact['items'] = _items

        return fact
