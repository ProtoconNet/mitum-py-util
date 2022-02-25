from ....hint import MBS_SIGN_DOCUMENTS_OP, MBS_SIGN_DOCUMENTS_OP_FACT
from ..fact import GeneralDocumentsFact
from ....common import _hint


class SignDocumentsFact(GeneralDocumentsFact):
    def __init__(self, sender, items):
        super(SignDocumentsFact, self).__init__(MBS_SIGN_DOCUMENTS_OP_FACT, sender, items)
        
    @property
    def operationHint(self):
        return _hint(MBS_SIGN_DOCUMENTS_OP)