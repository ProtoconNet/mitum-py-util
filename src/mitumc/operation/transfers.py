import base64

from mitumc.common import bconcat, _hint
from mitumc.hash import sha
from mitumc.hint import MC_TRANSFERS_ITEM_MULTI_AMOUNTS, MC_TRANSFERS_OP_FACT, MC_TRNASFERS_ITEM_SINGLE_AMOUNT
from mitumc.operation.base import OperationFact, Address

class TransfersItem(object):
    def __init__(self, receiver, amounts):
        if len(amounts) > 1:
            self.hint = _hint(MC_TRANSFERS_ITEM_MULTI_AMOUNTS)
        else:
            self.hint = _hint(MC_TRNASFERS_ITEM_SINGLE_AMOUNT)
        self.receiver = Address(receiver)
        self.amounts = amounts

    def dict(self):
        amounts = self.amounts

        bamounts = bytearray()
        for amount in amounts:
            bamounts += bytearray(amount.bytes())

        breceiver = self.receiver.bytes()
        bamounts = bytes(bamounts)
        
        return bconcat(breceiver, bamounts)

    def dict(self):
        item = {}
        item['_hint'] = self.hint.hint
        item['receiver'] = self.receiver.address
        
        _amounts = list()
        for _amount in self.amounts:
            _amounts.append(_amount.dict())
        item['amounts'] = _amounts

        return item


class TransfersFact(OperationFact):
    def __init__(self, sender, items):
        super(TransfersFact, self).__init__(_hint(MC_TRANSFERS_OP_FACT))
        self.sender = sender
        self.items = items
        self.hash = sha.sha3(self.bytes())

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
        fact['token'] = base64.b64encode(self.token.encode('ascii')).decode('ascii')
        fact['sender'] = self.sender.address

        _items = list()
        for _item in self.items:
            _items.append(_item.dict())
        fact['items'] = _items

        return fact
