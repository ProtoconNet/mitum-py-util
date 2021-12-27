import base64

from mitumc.common import bconcat, _hint
from mitumc.hash import sha
from mitumc.hint import MC_KEYUPDATER_OP_FACT
from mitumc.operation.base import OperationFact, Address


class KeyUpdaterFact(OperationFact):
    def __init__(self, target, keys, cid):
        super(KeyUpdaterFact, self).__init__(MC_KEYUPDATER_OP_FACT)
        self.target = Address(target)
        self.cid = cid
        self.keys = keys
        self.hash = sha.sha3(self.bytes())
    
    def bytes(self):
        btoken = self.token.encode()
        btarget = self.target.bytes()
        bkeys = self.keys.bytes()
        bcid = self.cid.encode()
      
        return bconcat(btoken, btarget, bkeys, bcid)
    
    def dict(self):
        fact = {}
        fact['_hint'] = self.hint.hint
        fact['hash'] = self.hash.hash
        fact['token'] = base64.b64encode(self.token.encode('ascii')).decode('ascii')
        fact['target'] = self.target.address
        fact['keys'] = self.keys.dict()
        fact['currency'] = self.cid
        return fact


