from .fact import CreateDocumentsFact, UpdateDocumentsFact
from .item import CreateDocumentsItem, UpdateDocumentsItem
from ..base import OperationGenerator
from .blocksign import BlockSignGenerator
from .blockcity import BlockCityGenerator

class DocumentGenerator(OperationGenerator):
    def __init__(self, id):
        super(DocumentGenerator, self).__init__(id)
        self.blocksign = BlockSignGenerator(id)
        self.blockcity = BlockCityGenerator(id)
        
    def setId(self, id):
        super().setId(id)
        self.blocksign = BlockSignGenerator(id)
        self.blockcity = BlockCityGenerator(id)
        
    def getCreateDocumentsItem(self, document, cid):
        return CreateDocumentsItem(document, cid)
    
    def getCreateDocumentsFact(self, sender, items):
        return CreateDocumentsFact(sender, items)
    
    def getUpdateDocumentsItem(self, document, cid):
        return UpdateDocumentsItem(document, cid)
    
    def getUpdateDocumentsFact(self, sender, items):
        return UpdateDocumentsFact(sender, items)
    