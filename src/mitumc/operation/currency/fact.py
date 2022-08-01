import base64

from ..base import GeneralOperationFact, PurposedOperationFact
from ...hash import sha3
from ...common import concatBytes, _hint
from ...key import Address
from ...hint import (
    MC_CREATE_ACCOUNTS_OP, MC_CREATE_ACCOUNTS_OP_FACT, MC_KEYUPDATER_OP, 
    MC_KEYUPDATER_OP_FACT, MC_TRANSFERS_OP, MC_TRANSFERS_OP_FACT
)


class CreateAccountsFact(GeneralOperationFact):
    def __init__(self, sender, items):
        super(CreateAccountsFact, self).__init__(MC_CREATE_ACCOUNTS_OP_FACT, sender, items)
        
    @property
    def operationHint(self):
        return _hint(MC_CREATE_ACCOUNTS_OP)


class KeyUpdaterFact(PurposedOperationFact):
    def __init__(self, target, keys, cid):
        super(KeyUpdaterFact, self).__init__(MC_KEYUPDATER_OP_FACT)
        self.target = Address(target)
        self.cid = cid
        self.keys = keys
        self.hash = sha3(self.bytes())

    @property    
    def operationHint(self):
        return _hint(MC_KEYUPDATER_OP)

    def bytes(self):
        bToken = self.token.encode()
        bTarget = self.target.bytes()
        bKeys = self.keys.bytes()
        bCid = self.cid.encode()

        return concatBytes(bToken, bTarget, bKeys, bCid)

    def dict(self):
        fact = {}
        fact['_hint'] = self.hint.hint
        fact['hash'] = self.hash.hash
        fact['token'] = base64.b64encode(
            self.token.encode('ascii')).decode('ascii')
        fact['target'] = self.target.address
        fact['keys'] = self.keys.dict()
        fact['currency'] = self.cid
        return fact


class TransfersFact(GeneralOperationFact):
    def __init__(self, sender, items):
        super(TransfersFact, self).__init__(MC_TRANSFERS_OP_FACT, sender, items)
        
    @property
    def operationHint(self):
        return _hint(MC_TRANSFERS_OP)
