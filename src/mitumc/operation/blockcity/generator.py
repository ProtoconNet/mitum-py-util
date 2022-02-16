from ...hint import MBC_CREATE_DOCUMENTS_ITEM, MBC_CREATE_DOCUMENTS_OP_FACT, MBC_UPDATE_DOCUMENTS_ITEM, MBC_UPDATE_DOCUMENTS_OP_FACT
from ..base import OperationGenerator
from .base import Candidate, Info, UserStatistics
from .document import HistoryDocument, LandDocument, UserDocument, VoteDocument
from .fact import BlockCityFact
from .item import BlockCityItem


class BlockCityGenerator(OperationGenerator):
    def __init__(self, id):
        super(BlockCityGenerator, self).__init__(id)

    def candidate(self, address, nickname, manifest, count):
        return Candidate(address, nickname, manifest, count)
    
    def info(self, docType, documentId):
        return Info(docType, documentId)
    
    def userStatistics(self, hp, strength, agility, dexterity, charisma, intelligence, vital):
        return UserStatistics(hp, strength, agility, dexterity, charisma, intelligence, vital)
    
    def userDocument(self, info, owner, gold, bankGold, userStatistics):
        return UserDocument(info, owner, gold, bankGold, userStatistics)
    
    def landDocument(self, info, owner, address, area, renter, account, rentDate, period):
        return LandDocument(info, owner, address, area, renter, account, rentDate, period)
    
    def voteDocument(self, info, owner, round, endVoteTime, candidates, bossName, account, termofoffice):
        return VoteDocument(info, owner, round, endVoteTime, candidates, bossName, account, termofoffice)
    
    def historyDocument(self, info, owner, name, account, date, usage, application):
        return HistoryDocument(info, owner, name, account, date, usage, application)
    
    def createCreateDocumentsItem(self, document, currencyId):
        return BlockCityItem(MBC_CREATE_DOCUMENTS_ITEM, document.docType, document, currencyId)
    
    def createUpdateDocumentsItem(self, document, currencyId):
        return BlockCityItem(MBC_UPDATE_DOCUMENTS_ITEM, document.docType, document, currencyId)
    
    def createCreateDocumentsFact(self, sender, items):
        return BlockCityFact(MBC_CREATE_DOCUMENTS_OP_FACT, sender, items)
    
    def createUpdateDocumentsFact(self, sender, items):
        return BlockCityFact(MBC_UPDATE_DOCUMENTS_OP_FACT, sender, items)