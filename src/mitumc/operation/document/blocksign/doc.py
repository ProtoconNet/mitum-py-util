from ....common import Int, concatBytes
from .info import BlockSignGeneralInfo
from ..base import Document


class BlockSignDocument(Document):
    def __init__(self, did, owner, fileHash, creator, title, size, signers):
        super(BlockSignDocument, self).__init__(BlockSignGeneralInfo(did), owner)
        self.fileHash = fileHash
        self.creator = creator
        self.title = title
        self.size = Int(int(size))
        self.signers = signers
        
    def bytes(self):
        bInfo = self.info.bytes()
        bOwner = self.owner.bytes()
        bFileHash = self.fileHash.encode()
        bCreator = self.creator.bytes()
        bTitle = self.title.encode()
        bSize = self.size.tight()
        
        listSigners = list(self.signers)
        listSigners.sort(key=lambda x: x.address.bytes())

        bSigners = bytearray()
        for signer in listSigners:
            bSigners += signer.bytes()
        bSigners = bytes(bSigners)
        
        return concatBytes(bInfo, bOwner, bFileHash, bCreator, bTitle, bSize, bSigners)
    
    def dict(self):
        doc = {}
        
        doc['_hint'] = self.hint.hint
        doc['info'] = self.info.dict()
        doc['owner'] = self.owner.address
        doc['filehash'] = self.fileHash
        doc['creator'] = self.creator.dict()
        doc['title'] = self.title
        doc['size'] = str(self.size.value)
        
        signers = []
        for signer in self.signers:
            signers.append(signer.dict())
        doc['signers'] = signers
        
        return doc