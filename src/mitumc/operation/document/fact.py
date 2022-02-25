from ...hint import (
    MD_CREATE_DOCUMENTS_OP, MD_CREATE_DOCUMENTS_OP_FACT,
    MD_UPDATE_DOCUMENTS_OP, MD_UPDATE_DOCUMENTS_OP_FACT
)
from ..base import GeneralOperationFact, PurposedOperationFact
from ...common import _hint


class GeneralDocumentsFact(GeneralOperationFact):
    pass


class PurposedDocumentsFact(PurposedOperationFact):
    pass


class CreateDocumentsFact(GeneralDocumentsFact):
    def __init__(self, sender, items):
        super(CreateDocumentsFact, self).__init__(MD_CREATE_DOCUMENTS_OP_FACT, sender, items)
        
    @property
    def operationHint(self):
        return _hint(MD_CREATE_DOCUMENTS_OP)
    
    
class UpdateDocumentsFact(GeneralDocumentsFact):
    def __init__(self, sender, items):
        super(UpdateDocumentsFact, self).__init__(MD_UPDATE_DOCUMENTS_OP_FACT, sender, items)
        
    @property
    def operationHint(self):
        return _hint(MD_UPDATE_DOCUMENTS_OP)