from mitumc.operation.base import OperationGenerator
from mitumc.operation.blocksign.item import CreateDocumentsItem, TransferDocumentsItem, SignDocumentsItem
from mitumc.operation.blocksign.fact import BlockSignFact


class BlockSignGenerator(OperationGenerator):
    def __init__(self, id):
        super(id)

    def createCreateDocumentsItem(self, filehash, did, signcode, title, size, cid, signers, signcodes):
        return CreateDocumentsItem(filehash, did, signcode, title, size, cid, signers, signcodes)

    def createSignDocumentsItem(self, owner, did, cid):
        return SignDocumentsItem(owner, did, cid)

    def createTransferDocumentsItem(self, owner, receiver, did, cid):
        return TransferDocumentsItem(owner, receiver, did, cid)

    def createBlockSignFact(self, type, sender, items):
        return BlockSignFact(type, sender, items)
