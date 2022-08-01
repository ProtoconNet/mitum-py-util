from .base import CollectionPolicy, CollectionRegisterForm, MintForm, NFTSigner, NFTSigners
from .item import ApproveItem, BurnItem, DelegateItem, MintItem, NFTSignItem, NFTTransferItem
from .fact import (
    ApproveFact, BurnFact, CollectionPolicyUpdaterFact, CollectionRegisterFact, 
    DelegateFact, MintFact, NFTSignFact, NFTTransferFact
)
from ..base import OperationGenerator


class NFTGenerator(OperationGenerator):
    def __init__(self, id):
        super(NFTGenerator, self).__init__(id)

    def signer(self, account, share, signed):
        return NFTSigner(account, share, signed)

    def signers(self, total, _signers):
        return NFTSigners(total, _signers)

    def collectionRegisterForm(self, target, symbol, name, royalty, uri, whites):
        return CollectionRegisterForm(target, symbol, name, royalty, uri, whites)

    def collectionPolicy(self, name, royalty, uri, whites):
        return CollectionPolicy(name, royalty, uri, whites)

    def mintForm(self, hash, uri, creators, copyrighters):
        return MintForm(hash, uri, creators, copyrighters)

    def getMintItem(self, collection, form, cid):
        return MintItem(collection, form, cid)

    def getTransferItem(self, receiver, nid, cid):
        return NFTTransferItem(receiver, nid, cid)

    def getBurnItem(self, nid, cid):
        return BurnItem(nid, cid)

    def getApproveItem(self, approved, nid, cid):
        return ApproveItem(approved, nid, cid)

    def getDelegateItem(self, collection, agent, mode, cid):
        return DelegateItem(collection, agent, mode, cid)

    def getSignItem(self, qualification, nid, cid):
        return NFTSignItem(qualification, nid, cid)

    def getCollectionRegisgerFact(self, sender, form, cid):
        return CollectionRegisterFact(sender, form, cid)

    def getCollectioPolicyUpdaterFact(self, sender, collection, policy, cid):
        return CollectionPolicyUpdaterFact(sender, collection, policy, cid)

    def getMintFact(self, sender, items):
        return MintFact(sender, items)

    def getTransferFact(self, sender, items):
        return NFTTransferFact(sender, items)

    def getBurnFact(self, sender, items):
        return BurnFact(sender, items)

    def getApproveFact(self, sender, items):
        return ApproveFact(sender, items)

    def getDelegateFact(self, sender, items):
        return DelegateFact(sender, items)

    def getSignFact(self, sender, items):
        return NFTSignFact(sender, items)