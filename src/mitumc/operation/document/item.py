from ..base import Item
from ...hint import MD_CREATE_DOCUMENTS_ITEM, MD_UPDATE_DOCUMENTS_ITEM
from ...common import concatBytes


class DocumentsItem(Item):
    pass


class GeneralDocumentsItem(DocumentsItem):
    def __init__(self, itemType, document, cid):
        super(GeneralDocumentsItem, self).__init__(itemType)
        self.document = document
        self.cid = cid
        
    def bytes(self):
        bDocument = self.document.bytes()
        bCid = self.cid.encode()
        return concatBytes(bDocument, bCid)
    
    def dict(self):
        item = {}
        item['_hint'] = self.hint.hint
        item['doc'] = self.document.dict()
        item['currency'] = self.cid
        return item
    

class PurposedDocumentsItem(DocumentsItem):
    pass


class CreateDocumentsItem(GeneralDocumentsItem):
    def __init__(self, document, cid):
        super(CreateDocumentsItem, self).__init__(MD_CREATE_DOCUMENTS_ITEM, document, cid)
        

class UpdateDocumentsItem(GeneralDocumentsItem):
    def __init__(self, document, cid):
        super(UpdateDocumentsItem, self).__init__(MD_UPDATE_DOCUMENTS_ITEM, document, cid)