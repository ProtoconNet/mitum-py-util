from mitumc.hint import MBC_CREATE_DOCUMENTS_ITEM, MBC_CREATE_DOCUMENTS_OP_FACT, MBC_UPDATE_DOCUMENTS_ITEM, MBC_UPDATE_DOCUMENTS_OP_FACT
from mitumc.operation.base import OperationGenerator
from mitumc.operation.blockcity.base import Candidate, Info, UserStatistics
from mitumc.operation.blockcity.document import HistoryDocument, LandDocument, UserDocument, VoteDocument
from mitumc.operation.blockcity.fact import BlockCityFact
from mitumc.operation.blockcity.item import BlockCityItem


class BlockCityGenerator(OperationGenerator):
    def __init__(self, id):
        super(BlockCityGenerator, self).__init__(id)

    def candidate(self, address, nickname, manifest):
        return Candidate(address, nickname, manifest)
    
    def info(docType, documentId):
        return Info(docType, documentId)
    
    def userStatistics(hp, strength, agility, dexterity, charisma, intelligence, vital):
        return UserStatistics(hp, strength, agility, dexterity, charisma, intelligence, vital)
    
    def userDocument(info, owner, gold, bankGold, userStatistics):
        return UserDocument(info, owner, gold, bankGold, userStatistics)
    
    def landDocument(info, owner, address, area, renter, account, rentDate, period):
        return LandDocument(info, owner, address, area, renter, account, rentDate, period)
    
    def voteDocument(info, owner, round, endVoteTime, candidates, bossName, account, termofoffice):
        return VoteDocument(info, owner, round, endVoteTime, candidates, bossName, account, termofoffice)
    
    def historyDocument(info, owner, name, account, date, usage, application):
        return HistoryDocument(info, owner, name, account, date, usage, application)
    
    def createDocumentsItem(document, currencyId):
        return BlockCityItem(MBC_CREATE_DOCUMENTS_ITEM, document.docType, document, currencyId)
    
    def updateDocumentsItem(document, currencyId):
        return BlockCityItem(MBC_UPDATE_DOCUMENTS_ITEM, document.docType, document, currencyId)
    
    def createCreateDocumentsFact(sender, items):
        return BlockCityFact(MBC_CREATE_DOCUMENTS_OP_FACT, sender, items)
    
    def createUpdateDocumentsFact(sender, items):
        return BlockCityFact(MBC_UPDATE_DOCUMENTS_OP_FACT, sender, items)