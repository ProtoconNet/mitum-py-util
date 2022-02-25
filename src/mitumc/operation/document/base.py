from ...key import Address
from ...hint import MD_DOCUMENT_INFO
from ...common import BytesFactor, MitumFactor, concatBytes, parseDocumentId, _hint


class DocumentId(BytesFactor):
    def __init__(self, did):
        self.id, self.type = parseDocumentId(did)
        
    @property
    def did(self):
        return self.id + self.type
    
    def bytes(self):
        return self.did.encode()
    

class Info(MitumFactor):
    def __init__(self, docType, did):
        self.hint = _hint(MD_DOCUMENT_INFO)
        self.docType = docType
        self.did = DocumentId(did)
    
    @property
    def idHint(self):
        assert False, 'Unimplemented function idHint; Info'
    
    def bytes(self):
        bDid = self.did.bytes()
        bDocType = self.docType.encode()
        return concatBytes(bDid, bDocType)
    
    def dict(self):
        docId = {}
        docId['_hint'] = self.idHint.hint
        docId['id'] = self.did.did
        
        info = {}
        info['_hint'] = self.hint.hint
        info['docid'] = docId
        info['doctype'] = self.docType
        
        return info
    
    
class Document(MitumFactor):
    def __init__(self, info, owner):
        self.hint = _hint(info.docType)
        self.info = info
        self.owner = Address(owner)