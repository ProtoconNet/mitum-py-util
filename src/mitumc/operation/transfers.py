import base64

from mitumc.common import bconcat
from mitumc.hash import sha
from mitumc.operation import OperationFact, OperationFactBody


class TransfersItem(object):
    """ Single TransfersItem.

    Attributes:
        h               (Hint): hint; MC_TRNASFERS_ITEM_SINGLE_AMOUNT
        Receiver        (Keys): Receiver Address
        amounts (List(Amount)): List of amounts
    """
    def __init__(self, h, receiver, amounts):
        self.h = h
        self.receiver = receiver
        self.amounts = amounts

    def to_bytes(self):
        # Returns concatenated [receiver, amounts] in byte format
        amounts = self.amounts

        bamounts = bytearray()
        for amount in amounts:
            bamounts += bytearray(amount.to_bytes())

        breceiver = self.receiver.hinted().encode()
        bamounts = bytes(bamounts)
        
        return bconcat(breceiver, bamounts)

    def to_dict(self):
        item = {}
        item['_hint'] = self.h.hint
        item['receiver'] = self.receiver.hinted()
        
        _amounts = list()
        for _amount in self.amounts:
            _amounts.append(_amount.to_dict())
        item['amounts'] = _amounts

        return item


class TransfersFactBody(OperationFactBody):
    """ Body of TransfersFact.

    Attributes:
        h                    (Hint): hint; MC_TRANSFERS_OP_FACT
        token                 (str): base64 encoded fact token
        sender            (Address): Sender address
        items (List(TransfersItem)): List of items
    """
    def __init__(self, h, token, sender, items):
        super(TransfersFactBody, self).__init__(h, token)
        self.sender = sender
        self.items = items

    def to_bytes(self):
        # Returns concatenated [token, sender, items] in byte format

        bitems = bytearray()
        for i in self.items:
            bitems += bytearray(i.to_bytes())

        btoken = self.token.encode()
        bsender = self.sender.hinted().encode()
        bitems = bytes(bitems)

        return bconcat(btoken, bsender, bitems)

    def generate_hash(self):
        return sha.sum256(self.to_bytes())


class TransfersFact(OperationFact):
    """ Contains TransfersFactBody and a hash.

    Attributes:
        hs                (Hash): Fact Hash
        body (TransfersFactbody): Fact body object
    """
    def __init__(self, hs, body):
        super(TransfersFact, self).__init__(hs, body)

    def to_dict(self):
        d = self.body
        fact = {}
        fact['_hint'] = d.h.hint
        fact['hash'] = self.hash().hash
        fact['token'] = base64.b64encode(d.token.encode('ascii')).decode('ascii')
        fact['sender'] = d.sender.hinted()

        _items = list()
        for _item in d.items:
            _items.append(_item.to_dict())
        fact['items'] = _items

        return fact
