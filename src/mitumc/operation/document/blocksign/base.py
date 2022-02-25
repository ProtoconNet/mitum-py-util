from ....key import Address
from ....hint import MBS_USER
from ....common import MitumFactor, _hint, concatBytes


class BlockSignUser(MitumFactor):
    def __init__(self, address, signCode, signed):
        self.hint = _hint(MBS_USER)
        self.address = Address(address)
        self.signCode = signCode
        self.signed = signed
        
    def bytes(self):
        bAddress = self.address.bytes()
        bSignCode = self.signCode.encode()
        
        bSigned = bytes(1)
        if self.signed:
            bSigned = bytes([1])
        else:
            bSigned = bytes([0])
        
        return concatBytes(bAddress, bSignCode, bSigned)
    
    def dict(self):
        user = {}
        user['_hint'] = self.hint.hint
        user['address'] = self.address.address
        user['signcode'] = self.signCode
        user['signed'] = self.signed
        return user