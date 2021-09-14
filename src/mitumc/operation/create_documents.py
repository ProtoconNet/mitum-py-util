import base64

from mitumc.common import bconcat
from mitumc.hash import sha
from mitumc.operation import OperationFact, OperationFactBody


class CreateDocumentsItem(object):
    def __init__(self, h, fh, did, signcode, title, size, cid, signers, signcodes):
        self.h = h
        self.fh = fh
        self.did = did
        self.signcode = signcode
        self.title = title
        self.size = size
        self.cid = cid
        self.signers = signers
        self.signcodes = signcodes

    def to_bytes(self):
        bfh = self.fh.encode()
        bdid = self.did.tight_bytes()
        bscode = self.signcode.encode()
        btitle = self.title.encode()
        bsize = self.size.tight_bytes()
        bcid = self.cid.encode()

        bsigners = bytearray()
        for s in self.signers:
            bsigners += bytearray(s.encode())
        bsigners = bytes(bsigners)
        
        bscodes = bytearray()
        for sc in self.signcodes:
            bscodes += bytearray(sc.encode())
        bscodes = bytes(bscodes)

        return bconcat(bfh, bdid, bscode, btitle, bsize, bcid, bsigners, bscodes)

    def to_dict(self):
        item = {}
        item['_hint'] = self.h.hint
        item['filehash'] = self.fh
        item['documentid'] = str(self.did.value)
        item['signcode'] = self.signcode
        item['title'] = self.title
        item['size'] = str(self.size.value)
        item['signers'] = self.signers
        item['signcodes'] = self.signcodes
        item['currency'] = self.cid
        return item


class CreateDocumentsFactBody(OperationFactBody):
    def __init__(self, h, token, sender, items):
        super(CreateDocumentsFactBody, self).__init__(h, token)
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


class CreateDocumentsFact(OperationFact):
    def __init__(self, net_id, hs, body):
        super(CreateDocumentsFact, self).__init__(net_id, hs, body)

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
        