from ...hint import MBS_CREATE_DOCUMENTS_OP_FACT, MBS_SIGN_DOCUMENTS_OP_FACT
from ..base import OperationGenerator
from .item import CreateDocumentsItem, SignDocumentsItem
from .fact import BlockSignFact
from .base import BLOCKSIGN_CREATE_DOCUMENTS, BLOCKSIGN_SIGN_DOCUMENTS


class BlockSignGenerator(OperationGenerator):
    def __init__(self, id):
        super(BlockSignGenerator, self).__init__(id)

    def createCreateDocumentsItem(self, filehash, did, signcode, title, size, cid, signers, signcodes):
        return CreateDocumentsItem(filehash, did, signcode, title, size, cid, signers, signcodes)

    def createSignDocumentsItem(self, owner, did, cid):
        return SignDocumentsItem(owner, did, cid)

    def createBlockSignFact(self, type, sender, items):
        if type == BLOCKSIGN_CREATE_DOCUMENTS:
            _type = MBS_CREATE_DOCUMENTS_OP_FACT
        elif type == BLOCKSIGN_SIGN_DOCUMENTS:
            _type = MBS_SIGN_DOCUMENTS_OP_FACT
        return BlockSignFact(_type, sender, items)
