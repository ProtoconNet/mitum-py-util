from .doc import HistoryDocument, LandDocument, UserDocument, VoteDocument
from .base import Candidate, UserStatistics
from ...base import OperationGenerator


class BlockCityGenerator(OperationGenerator):
    def __init__(self, id):
        super(BlockCityGenerator, self).__init__(id)

    def candidate(self, address, nickname, manifest, count):
        return Candidate(address, nickname, manifest, count)
    
    def userStatistics(self, hp, strength, agility, dexterity, charisma, intelligence, vital):
        return UserStatistics(hp, strength, agility, dexterity, charisma, intelligence, vital)
    
    def userDocument(self, did, owner, gold, bankGold, userStatistics):
        return UserDocument(did, owner, gold, bankGold, userStatistics)
    
    def landDocument(self, did, owner, address, area, renter, account, rentDate, period):
        return LandDocument(did, owner, address, area, renter, account, rentDate, period)
    
    def voteDocument(self, did, owner, round, endVoteTime, candidates, bossName, account, termofoffice):
        return VoteDocument(did, owner, round, endVoteTime, candidates, bossName, account, termofoffice)
    
    def historyDocument(self, did, owner, name, account, date, usage, application):
        return HistoryDocument(did, owner, name, account, date, usage, application)