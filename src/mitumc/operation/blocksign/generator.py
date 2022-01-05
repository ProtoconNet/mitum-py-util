from mitumc.hint import MBS_CREATE_DOCUMENTS_OP_FACT, MBS_SIGN_DOCUMENTS_OP_FACT, MBS_TRANSFER_DOCUMENTS_OP_FACT
from mitumc.operation.base import OperationGenerator
from mitumc.operation.blocksign.item import CreateDocumentsItem, TransferDocumentsItem, SignDocumentsItem
from mitumc.operation.blocksign.fact import BlockSignFact
from mitumc.operation.blocksign.base import BLOCKSIGN_CREATE_DOCUMENTS, BLOCKSIGN_SIGN_DOCUMENTS, BLOCKSIGN_TRANSFER_DOCUMENTS


class BlockSignGenerator(OperationGenerator):
    def __init__(self, id):
        super(BlockSignGenerator, self).__init__(id)

    def createCreateDocumentsItem(self, filehash, did, signcode, title, size, cid, signers, signcodes):
        return CreateDocumentsItem(filehash, did, signcode, title, size, cid, signers, signcodes)

    def createSignDocumentsItem(self, owner, did, cid):
        return SignDocumentsItem(owner, did, cid)

    def createTransferDocumentsItem(self, owner, receiver, did, cid):
        return TransferDocumentsItem(owner, receiver, did, cid)

    def createBlockSignFact(self, type, sender, items):
        if type == BLOCKSIGN_CREATE_DOCUMENTS:
            _type = MBS_CREATE_DOCUMENTS_OP_FACT
        elif type == BLOCKSIGN_TRANSFER_DOCUMENTS:
            _type = MBS_TRANSFER_DOCUMENTS_OP_FACT
        elif type == BLOCKSIGN_SIGN_DOCUMENTS:
            _type = MBS_SIGN_DOCUMENTS_OP_FACT
        return BlockSignFact(_type, sender, items)
