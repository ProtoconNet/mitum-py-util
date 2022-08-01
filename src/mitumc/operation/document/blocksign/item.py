from ..base import DocumentId
from ..item import PurposedDocumentsItem
from ....common import concatBytes
from ....hint import MBS_SIGN_ITEM_SINGLE_DOCUMENT
from ....key import Address


class SignDocumentsItem(PurposedDocumentsItem):
    def __init__(self, did, owner, cid):
        super(SignDocumentsItem, self).__init__(MBS_SIGN_ITEM_SINGLE_DOCUMENT)
        self.did = DocumentId(did)
        self.owner = Address(owner)
        self.cid = cid
        
    def bytes(self):
        bDid = self.did.bytes()
        bOwner = self.owner.bytes()
        bCid = self.cid.encode()
        return concatBytes(bDid, bOwner, bCid)
    
    def dict(self):
        item = {}
        item['_hint'] = self.hint.hint
        item['documentid'] = self.did.did
        item['owner'] = self.owner.address
        item['currency'] = self.cid