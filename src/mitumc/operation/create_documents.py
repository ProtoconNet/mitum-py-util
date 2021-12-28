import base64

from mitumc.common import bconcat, _hint, Int
from mitumc.hash import sha3
from mitumc.hint import MBS_CREATE_DOCUMENTS_OP_FACT, MBS_CREATE_DOCUMENTS_SINGLE_FILE
from mitumc.operation.base import OperationFact, Address


class CreateDocumentsItem(object):
    def __init__(self, fileHash, did, signcode, title, size, cid, signers, signcodes):
        self.hint = _hint(MBS_CREATE_DOCUMENTS_SINGLE_FILE)
        self.fileHash = fileHash
        self.did = Int(did)
        self.signcode = signcode
        self.title = title
        self.size = Int(size)
        self.cid = cid
        self.signers = signers
        self.signcodes = signcodes

    def bytes(self):
        bfh = self.fileHash.encode()
        bdid = self.did.tight()
        bscode = self.signcode.encode()
        btitle = self.title.encode()
        bsize = self.size.tight()
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

    def dict(self):
        item = {}
        item['_hint'] = self.hint.hint
        item['filehash'] = self.fileHash
        item['documentid'] = str(self.did.value)
        item['signcode'] = self.signcode
        item['title'] = self.title
        item['size'] = str(self.size.value)
        item['signers'] = self.signers
        item['signcodes'] = self.signcodes
        item['currency'] = self.cid
        return item


class CreateDocumentsFact(OperationFact):
    def __init__(self, sender, items):
        super(CreateDocumentsFact, self).__init__(MBS_CREATE_DOCUMENTS_OP_FACT)
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
        