import base64

from mitumc.common import bconcat
from mitumc.hash import sha
from mitumc.operation import OperationFact, OperationFactBody


class TransferDocumentsItem(object):
    def __init__(self, h, owner, receiver, did, cid):
        self.h = h
        self.owner = owner
        self.receiver = receiver
        self.did = did
        self.cid = cid

    def to_bytes(self):
        bdid = self.did.tight_bytes()
        bowner = self.owner.hinted().encode()
        breceiver = self.receiver.hinted().encode()
        bcid = self.cid.encode()
        return bconcat(bdid, bowner, breceiver, bcid)

    def to_dict(self):
        item = {}
        item['_hint'] = self.h.hint
        item['documentid'] = str(self.did.value)
        item['owner'] = self.owner.hinted()
        item['receiver'] = self.receiver.hinted()
        item['currency'] = self.cid
        return item


class TransferDocumentsFactBody(OperationFactBody):
    def __init__(self, h, token, sender, items):
        super(TransferDocumentsFactBody, self).__init__(h, token)
        self.sender = sender
        self.items = items

    def to_bytes(self):
        bitems = bytearray()
        for i in self.items:
            bitems += bytearray(i.to_bytes())
        
        btoken = self.token.encode()
        bsender = self.sender.hinted().encode()
        bitems = bytes(bitems)

        return bconcat(btoken, bsender, bitems)

    def generate_hash(self):
        return sha.sum256(self.to_bytes())


class TransferDocumentsFact(OperationFact):
    def __init__(self, net_id, hs, body):
        super(TransferDocumentsFact, self).__init__(net_id, hs, body)

    def hash(self):
        return self.hs

    def to_dict(self):
        d = self.body
        fact = {}
        fact['_hint'] = d.h.hint
        fact['hash'] = self.hash().hash
        token = base64.b64encode(d.token.encode('ascii')).decode('ascii')
        fact['token'] = token
        fact['sender'] = d.sender.hinted()

        _items = list()
        for item in d.items:
            _items.append(item.to_dict())
        fact['items'] = _items
        return fact
        