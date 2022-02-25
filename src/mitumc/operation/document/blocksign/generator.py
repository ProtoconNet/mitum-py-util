from .fact import SignDocumentsFact
from .item import SignDocumentsItem
from .doc import BlockSignDocument
from .base import BlockSignUser
from ...base import OperationGenerator


class BlockSignGenerator(OperationGenerator):
    def __init__(self, id):
        super(BlockSignGenerator, self).__init__(id)
        
    def user(self, address, signCode, signed):
        return BlockSignUser(address, signCode, signed)
    
    def document(self, did, owner, fileHash, creator, title, size, signers):
        return BlockSignDocument(did, owner, fileHash, creator, title, size, signers)
    
    def getSignDocumentsItem(self, did, owner, cid):
        return SignDocumentsItem(did, owner, cid)
    
    def getSignDocumentsFact(self, sender, items):
        return SignDocumentsFact(sender, items)