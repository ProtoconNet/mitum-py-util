import base64

from mitumc.common import bconcat, _hint, Int
from mitumc.hash import sha
from mitumc.hint import MBS_SIGN_DOCUMENTS_OP_FACT, MBS_SIGN_ITEM_SINGLE_DOCUMENT
from mitumc.operation.base import OperationFact, Address


class SignDocumentsItem(object):
    def __init__(self, owner, did, cid):
        self.hint = _hint(MBS_SIGN_ITEM_SINGLE_DOCUMENT)
        self.did = Int(did)
        self.owner = Address(owner)
        self.cid = cid

    def to_bytes(self):
        bdid = self.did.tight()
        bowner = self.owner.bytes()
        bcid = self.cid.encode()
        return bconcat(bdid, bowner, bcid)

    def to_dict(self):
        item = {}
        item['_hint'] = self.hint.hint
        item['documentid'] = str(self.did.value)
        item['owner'] = self.owner.address
        item['currency'] = self.cid
        return item


class SignDocumentsFact(OperationFact):
    def __init__(self, sender, items):
        super(SignDocumentsFact, self).__init__(_hint(MBS_SIGN_DOCUMENTS_OP_FACT))
        self.sender = Address(sender)
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
        token = base64.b64encode(self.token.encode('ascii')).decode('ascii')
        fact['token'] = token
        fact['sender'] = self.sender.address

        _items = list()
        for item in self.items:
            _items.append(item.dict())
        fact['items'] = _items
        return fact
        