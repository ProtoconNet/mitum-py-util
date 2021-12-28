import base64

from mitumc.common import bconcat, _hint, Int
from mitumc.hash import sha3
from mitumc.hint import MBS_TRANSFER_DOCUMENTS_OP_FACT, MBS_TRANSFER_ITEM_SINGLE_DOCUMENT
from mitumc.operation.base import OperationFact, Address


class TransferDocumentsItem(object):
    def __init__(self, owner, receiver, did, cid):
        self.hint = _hint(MBS_TRANSFER_ITEM_SINGLE_DOCUMENT)
        self.owner = Address(owner)
        self.receiver = Address(receiver)
        self.did = Int(did)
        self.cid = cid

    def bytes(self):
        bdid = self.did.tight()
        bowner = self.owner.bytes()
        breceiver = self.receiver.bytes()
        bcid = self.cid.encode()
        return bconcat(bdid, bowner, breceiver, bcid)

    def dict(self):
        item = {}
        item['_hint'] = self.hint.hint
        item['documentid'] = str(self.did.value)
        item['owner'] = self.owner.address
        item['receiver'] = self.receiver.address
        item['currency'] = self.cid
        return item


class TransferDocumentsFact(OperationFact):
    def __init__(self, sender, items):
        super(TransferDocumentsFact, self).__init__(MBS_TRANSFER_DOCUMENTS_OP_FACT)
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
    
        