from ..base import Info
from ....hint import MBS_DOCTYPE_DOCUMENT_DATA, MD_DOCUMENT_ID
from ....common import _hint

class BlockSignInfo(Info):
    @property
    def idHint(self):
        if self.docType == MBS_DOCTYPE_DOCUMENT_DATA:
            return _hint(MD_DOCUMENT_ID)
        assert False, 'Invalid document type; BlockSignInfo.idHint'
        

class BlockSignGeneralInfo(BlockSignInfo):
    def __init__(self, did):
        super(BlockSignGeneralInfo, self).__init__(MBS_DOCTYPE_DOCUMENT_DATA, did)
        