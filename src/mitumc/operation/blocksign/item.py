from mitumc.common import _hint, concat, Int
from mitumc.key import Address

from mitumc.operation.blocksign.hint import (
    MBS_CREATE_DOCUMENTS_SINGLE_FILE, MBS_TRANSFER_ITEM_SINGLE_DOCUMENT, MBS_SIGN_ITEM_SINGLE_DOCUMENT)


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
        bDid = self.did.tight()
        bSignCode = self.signcode.encode()
        bTitle = self.title.encode()
        bSize = self.size.tight()
        bCid = self.cid.encode()

        bSigners = bytearray()
        for s in self.signers:
            bSigners += bytearray(s.encode())
        bSigners = bytes(bSigners)

        bSignCodes = bytearray()
        for sc in self.signcodes:
            bSignCodes += bytearray(sc.encode())
        bSignCodes = bytes(bSignCodes)

        return concat(bfh, bDid, bSignCode, bTitle, bSize, bCid, bSigners, bSignCodes)

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


class TransferDocumentsItem(object):
    def __init__(self, owner, receiver, did, cid):
        self.hint = _hint(MBS_TRANSFER_ITEM_SINGLE_DOCUMENT)
        self.owner = Address(owner)
        self.receiver = Address(receiver)
        self.did = Int(did)
        self.cid = cid

    def bytes(self):
        bDid = self.did.tight()
        bOwner = self.owner.bytes()
        bReceiver = self.receiver.bytes()
        bCid = self.cid.encode()
        return concat(bDid, bOwner, bReceiver, bCid)

    def dict(self):
        item = {}
        item['_hint'] = self.hint.hint
        item['documentid'] = str(self.did.value)
        item['owner'] = self.owner.address
        item['receiver'] = self.receiver.address
        item['currency'] = self.cid
        return item


class SignDocumentsItem(object):
    def __init__(self, owner, did, cid):
        self.hint = _hint(MBS_SIGN_ITEM_SINGLE_DOCUMENT)
        self.did = Int(did)
        self.owner = Address(owner)
        self.cid = cid

    def bytes(self):
        bDid = self.did.tight()
        bOwner = self.owner.bytes()
        bCid = self.cid.encode()
        return concat(bDid, bOwner, bCid)

    def dict(self):
        item = {}
        item['_hint'] = self.hint.hint
        item['documentid'] = str(self.did.value)
        item['owner'] = self.owner.address
        item['currency'] = self.cid
        return item