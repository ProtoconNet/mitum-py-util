from .base import NFTID
from ..base import Item
from ...common import concatBytes, parseNFTId
from ...key import Address
from ...hint import (
    MNFT_APPROVE_ITEM, MNFT_BURN_ITEM, MNFT_DELEGATE_ITEM, 
    MNFT_MINT_ITEM, MNFT_SIGN_ITEM, MNFT_TRANSFER_ITEM
)


class NFTItem(Item):
    def __init__(self, itemType, cid):
        super(NFTItem, self).__init__(itemType)
        self.cid = cid


class MintItem(NFTItem):
    def __init__(self, collection, form, cid):
        super(MintItem, self).__init__(MNFT_MINT_ITEM, cid)
        self.collection = collection
        self.form = form

    def bytes(self):
        bCollection = self.collection.encode()
        bForm = self.form.bytes()
        bCid = self.cid.encode()
        return concatBytes(bCollection, bForm, bCid)

    def dict(self):
        item = {}
        item['_hint'] = self.hint.hint
        item['collection'] = self.collection
        item['form'] = self.form.dict()
        item['currency'] = self.cid
        return item


class NFTTransferItem(NFTItem):
    def __init__(self, receiver, nid, cid):
        super(NFTTransferItem, self).__init__(MNFT_TRANSFER_ITEM, cid)
        c, id = parseNFTId(nid)
        self.nid = NFTID(c, id)
        self.receiver = Address(receiver)

    def bytes(self):
        bReceiver = self.receiver.bytes()
        bNid = self.nid.bytes()
        bCid = self.cid.encode()
        return concatBytes(bReceiver, bNid, bCid)

    def dict(self):
        item = {}
        item['_hint'] = self.hint.hint
        item['receiver'] = self.receiver.address
        item['nft'] = self.nid.dict()
        item['currency'] = self.cid
        return item


class BurnItem(NFTItem):
    def __init__(self, nid, cid):
        super(BurnItem, self).__init__(MNFT_BURN_ITEM, cid)
        c, id = parseNFTId(nid)
        self.nid = NFTID(c, id)

    def bytes(self):
        bNid = self.nid.bytes()
        bCid = self.cid.encode()
        return concatBytes(bNid, bCid)

    def dict(self):
        item = {}
        item['_hint'] = self.hint.hint
        item['nft'] = self.nid.dict()
        item['currency'] = self.cid
        return item


class ApproveItem(NFTItem):
    def __init__(self, approved, nid, cid):
        super(ApproveItem, self).__init__(MNFT_APPROVE_ITEM, cid)
        self.approved = Address(approved)
        c, id = parseNFTId(nid)
        self.nid = NFTID(c, id)

    def bytes(self):
        bApproved = self.approved.bytes()
        bNid = self.nid.bytes()
        bCid = self.cid.encode()
        return concatBytes(bApproved, bNid, bCid)

    def dict(self):
        item = {}
        item['_hint'] = self.hint.hint
        item['approved'] = self.approved.address
        item['nft'] = self.nid.dict()
        item['currency'] = self.cid
        return item


class DelegateItem(NFTItem):
    def __init__(self, collection, agent, mode, cid):
        super(DelegateItem, self).__init__(MNFT_DELEGATE_ITEM, cid)
        self.collection = collection
        self.agent = Address(agent)
        self.mode = mode
    
    def bytes(self):
        bCollection = self.collection.encode()
        bAgent = self.agent.bytes()
        bMode = self.mode.encode()
        bCid = self.cid.encode()
        return concatBytes(bCollection, bAgent, bMode, bCid)

    def dict(self):
        item = {}
        item['_hint'] = self.hint.hint
        item['collection'] = self.collection
        item['agent'] = self.agent.address
        item['mode'] = self.mode
        item['currency'] = self.cid
        return item


class NFTSignItem(NFTItem):
    def __init__(self, qualification, nid, cid):
        super(NFTSignItem, self).__init__(MNFT_SIGN_ITEM, cid)
        self.qualification = qualification
        c, id = parseNFTId(nid)
        self.nid = NFTID(c, id)
        
    def bytes(self):
        bQual = self.qualification.encode()
        bNid = self.nid.bytes()
        bCid = self.cid.encode()
        return concatBytes(bQual, bNid, bCid)

    def dict(self):
        item = {}
        item['_hint'] = self.hint.hint
        item['qualification'] = self.qualification
        item['nft'] = self.nid.dict()
        item['currency'] = self.cid
        return item
