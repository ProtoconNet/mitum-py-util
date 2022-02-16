from ...common import Int, parseDocumentId, _hint
from ...hint import (MBC_DOCTYPE_HISTORY_DATA, MBC_DOCTYPE_LAND_DATA, MBC_DOCTYPE_USER_DATA, MBC_DOCTYPE_VOTE_DATA, 
                         MBC_DOCUMENT_INFO, MBC_HISTORY_DOCUMENT_ID, MBC_LAND_DOCUMENT_ID, MBC_USER_DOCUMENT_ID, MBC_USER_STATISTICS,
                         MBC_VOTE_DOCUMENT_ID, MBC_VOTING_CANDIDATE)
from ...common import concatBytes
from ...key import Address


class DocumentId(object):
    def __init__(self, documentId):
        _id, self.type = parseDocumentId(documentId)
        self.id = _id
        
    @property
    def docId(self):
        return self.id + self.type
    
    @property
    def type(self):
        return self.type
    
    def bytes(self):
        return self.docId.encode()
    

class Info(object):
    def __init__(self, docType, documentId):
        self.hint = _hint(MBC_DOCUMENT_INFO)
        self.docType = docType
        self.documentId = DocumentId(documentId)
        
    def bytes(self):
        bDocumentId = self.documentId.bytes()
        bDocType = self.docType.encode()
        return concatBytes(bDocumentId, bDocType)
    
    def dict(self):
        docId = {}
        
        if self.docType == MBC_DOCTYPE_USER_DATA:
            docId['_hint'] = _hint(MBC_USER_DOCUMENT_ID)
        elif self.docType == MBC_DOCTYPE_LAND_DATA:
            docId['_hint'] = _hint(MBC_LAND_DOCUMENT_ID)
        elif self.docType == MBC_DOCTYPE_VOTE_DATA:
            docId['_hint'] = _hint(MBC_VOTE_DOCUMENT_ID)
        elif self.docType == MBC_DOCTYPE_HISTORY_DATA:
            docId['_hint'] = _hint(MBC_HISTORY_DOCUMENT_ID)
        else:
            raise Exception("Invalid document type; Info.dict()")
        
        docId['id'] = self.documentId.docId
        
        info = {}
        
        info['_hint'] = self.hint.hint
        info['docid'] = docId
        info['doctype'] = self.docType
        
        return info
        
        
class Candidate(object):
    def __init__(self, address, nickname, manifest, count):
        assert len(manifest) <= 100, 'manifest length is over 100! (len(manifest) <= 100); Candidate.__init__(address, manifest)'
        
        self.hint = _hint(MBC_VOTING_CANDIDATE)
        self.address = Address(address)
        self.nickname = nickname
        self.manifest = manifest
        self.count = Int(count)
        
    def bytes(self):
        bAddress = self.address.bytes()
        bNickname = self.nickname.encode()
        bManifest = self.manifest.encode()
        bCount = self.count.bytes()
        return concatBytes(bAddress, bNickname, bManifest, bCount)
    
    def dict(self):
        candidate = {}
        
        candidate['_hint'] = self.hint.hint
        candidate['address'] = self.address.address
        candidate['nickname'] = self.nickname
        candidate['manifest'] = self.manifest
        candidate['count'] = self.count.value
        
        return candidate
    

class UserStatistics(object):
    def __init__(self, hp, str, agi, dex, cha, intel, vital):
        self.hint = _hint(MBC_USER_STATISTICS)
        self.hp = Int(hp)
        self.str = Int(str)
        self.agi = Int(agi)
        self.dex = Int(dex)
        self.cha = Int(cha)
        self.intel = Int(intel)
        self.vital = Int(vital)
        
    def bytes(self):
        return concatBytes(
            self.hp.bytes(),
            self.str.bytes(),
            self.agi.bytes(),
            self.dex.bytes(),
            self.cha.bytes(),
            self.intel.bytes(),
            self.vital.bytes()
        )
    
    def dict(self):
        statistics = {}
        
        statistics['_hint'] = self.hint.hint
        statistics['hp'] = self.hp.value
        statistics['strength'] = self.str.value
        statistics['agility'] = self.agi.value
        statistics['dexterity'] = self.dex.value
        statistics['charisma'] = self.cha.value
        statistics['intelligence'] = self.intel.value
        statistics['vital'] = self.vital.value
        
        return statistics