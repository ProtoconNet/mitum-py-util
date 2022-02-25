from ....key import Address
from ....hint import MBC_USER_STATISTICS, MBC_VOTING_CANDIDATE
from ....common import Int, MitumFactor, _hint, concatBytes


class Candidate(MitumFactor):
    def __init__(self, address, nickname, manifest, count):
        assert len(manifest) <= 100, 'manifest length is over 100! (len(manifest) <= 100); Candidate.__init__'
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