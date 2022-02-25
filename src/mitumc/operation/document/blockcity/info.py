from ....hint import MBC_DOCTYPE_HISTORY_DATA, MBC_DOCTYPE_LAND_DATA, MBC_DOCTYPE_USER_DATA, MBC_DOCTYPE_VOTE_DATA, MBC_HISTORY_DOCUMENT_ID, MBC_LAND_DOCUMENT_ID, MBC_USER_DOCUMENT_ID, MBC_VOTE_DOCUMENT_ID
from ..base import Info
from ....common import _hint


class BlockCityInfo(Info):
    @property
    def idHint(self):
        if self.docType == MBC_DOCTYPE_USER_DATA:
            return _hint(MBC_USER_DOCUMENT_ID)
        if self.docType == MBC_DOCTYPE_LAND_DATA:
            return _hint(MBC_LAND_DOCUMENT_ID)
        if self.docType == MBC_DOCTYPE_VOTE_DATA:
            return _hint(MBC_VOTE_DOCUMENT_ID)
        if self.docType == MBC_DOCTYPE_HISTORY_DATA:
            return _hint(MBC_HISTORY_DOCUMENT_ID)
        assert False, 'Invalid document type; BlockCityInfo.idHint'
        

class BlockCityUserInfo(BlockCityInfo):
    def __init__(self, did):
        super(BlockCityUserInfo, self).__init__(MBC_DOCTYPE_USER_DATA, did)


class BlockCityLandInfo(BlockCityInfo):
    def __init__(self, did):
        super(BlockCityLandInfo, self).__init__(MBC_DOCTYPE_LAND_DATA, did)
        

class BlockCityVoteInfo(BlockCityInfo):
    def __init__(self, did):
        super(BlockCityVoteInfo, self).__init__(MBC_DOCTYPE_VOTE_DATA, did)
        

class BlockCityHistoryInfo(BlockCityInfo):
    def __init__(self, did):
        super(BlockCityHistoryInfo, self).__init__(MBC_DOCTYPE_HISTORY_DATA, did)
        
