import base64
from ..base import GeneralOperationFact, PurposedOperationFact
from ...common import _hint, concatBytes
from ...key import Address
from ...hash import sha3
from ...hint import (
    MNFT_APPROVE_OP, MNFT_APPROVE_OP_FACT, MNFT_BURN_OP, MNFT_BURN_OP_FACT, MNFT_COLLECTION_POLICY_UPDATER_OP, 
    MNFT_COLLECTION_POLICY_UPDATER_OP_FACT, MNFT_COLLECTION_REGISTER_OP, MNFT_COLLECTION_REGISTER_OP_FACT, 
    MNFT_DELEGATE_OP, MNFT_DELEGATE_OP_FACT, MNFT_MINT_OP, MNFT_MINT_OP_FACT, MNFT_SIGN_OP, MNFT_SIGN_OP_FACT, 
    MNFT_TRANSFER_OP, MNFT_TRANSFER_OP_FACT
)


class CollectionRegisterFact(PurposedOperationFact):
    def __init__(self, sender, form, cid):
        super(CollectionRegisterFact, self).__init__(
            MNFT_COLLECTION_REGISTER_OP_FACT)
        self.sender = Address(sender)
        self.form = form
        self.cid = cid
        self.hash = sha3(self.bytes())

    @property
    def operationHint(self):
        return _hint(MNFT_COLLECTION_REGISTER_OP)

    def bytes(self):
        bToken = self.token.encode()
        bSender = self.sender.bytes()
        bForm = self.form.bytes()
        bCid = self.cid.encode()
        return concatBytes(bToken, bSender, bForm, bCid)

    def dict(self):
        fact = {}
        fact['_hint'] = self.hint.hint
        fact['hash'] = self.hash.hash
        fact['token'] = base64.b64encode(
            self.token.encode('ascii')).decode('ascii')
        fact['sender'] = self.sender.address
        fact['form'] = self.form.dict()
        fact['currency'] = self.cid
        return fact


class CollectionPolicyUpdaterFact(PurposedOperationFact):
    def __init__(self, sender, collection, policy, cid):
        super(CollectionPolicyUpdaterFact, self).__init__(
            MNFT_COLLECTION_POLICY_UPDATER_OP_FACT)
        self.sender = Address(sender)
        self.collection = collection
        self.policy = policy
        self.cid = cid
        self.hash = sha3(self.bytes())

    @property
    def operationHint(self):
        return _hint(MNFT_COLLECTION_POLICY_UPDATER_OP)

    def bytes(self):
        bToken = self.token.encode()
        bSender = self.sender.bytes()
        bCollection = self.collection.encode()
        bPolicy = self.policy.bytes()
        bCid = self.cid.encode()
        return concatBytes(bToken, bSender, bCollection, bPolicy, bCid)

    def dict(self):
        fact = {}
        fact['_hint'] = self.hint.hint
        fact['hash'] = self.hash.hash
        fact['token'] = base64.b64encode(
            self.token.encode('ascii')).decode('ascii')
        fact['sender'] = self.sender.address  
        fact['collection'] = self.collection
        fact['policy'] = self.policy.dict()
        fact['currency'] = self.cid
        return fact


class MintFact(GeneralOperationFact):
    def __init__(self, sender, items):
        super(MintFact, self).__init__(MNFT_MINT_OP_FACT, sender, items)
        
    @property
    def operationHint(self):
        return _hint(MNFT_MINT_OP)


class NFTTransferFact(GeneralOperationFact):
    def __init__(self, sender, items):
        super(NFTTransferFact, self).__init__(MNFT_TRANSFER_OP_FACT, sender, items)
        
    @property
    def operationHint(self):
        return _hint(MNFT_TRANSFER_OP)


class BurnFact(GeneralOperationFact):
    def __init__(self, sender, items):
        super(BurnFact, self).__init__(MNFT_BURN_OP_FACT, sender, items)
        
    @property
    def operationHint(self):
        return _hint(MNFT_BURN_OP)


class ApproveFact(GeneralOperationFact):
    def __init__(self, sender, items):
        super(ApproveFact, self).__init__(MNFT_APPROVE_OP_FACT, sender, items)
        
    @property
    def operationHint(self):
        return _hint(MNFT_APPROVE_OP)


class DelegateFact(GeneralOperationFact):
    def __init__(self, sender, items):
        super(DelegateFact, self).__init__(MNFT_DELEGATE_OP_FACT, sender, items)
        
    @property
    def operationHint(self):
        return _hint(MNFT_DELEGATE_OP)


class NFTSignFact(GeneralOperationFact):
    def __init__(self, sender, items):
        super(NFTSignFact, self).__init__(MNFT_SIGN_OP_FACT, sender, items)
        
    @property
    def operationHint(self):
        return _hint(MNFT_SIGN_OP)

