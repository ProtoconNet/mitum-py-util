import base64

from mitumc.hash import sha3
from mitumc.common import concatBytes
from mitumc.key import Address

from mitumc.operation.base import OperationFact


class BlockSignFact(OperationFact):
    def __init__(self, type, sender, items):
        super(BlockSignFact, self).__init__(type)
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
