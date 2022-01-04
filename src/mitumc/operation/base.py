import json

from mitumc.common import (_hint, concat, iso8601TimeStamp)
from mitumc.hash import sha3
from mitumc.sign import newFactSign

from mitumc.operation.blocksign import BLOCKSIGN_CREATE_DOCUMENTS, BLOCKSIGN_SIGN_DOCUMENTS, BLOCKSIGN_TRANSFER_DOCUMENTS
from mitumc.operation.blocksign.hint import MBS_CREATE_DOCUMENTS_OP_FACT, MBS_SIGN_DOCUMENTS_OP_FACT, MBS_TRANSFER_DOCUMENTS_OP_FACT

class OperationFact(object):
    def __init__(self, hint):
        _type = hint
        if hint == BLOCKSIGN_CREATE_DOCUMENTS:
            _type = MBS_CREATE_DOCUMENTS_OP_FACT
        elif hint == BLOCKSIGN_TRANSFER_DOCUMENTS:
            _type = MBS_TRANSFER_DOCUMENTS_OP_FACT
        elif hint == BLOCKSIGN_SIGN_DOCUMENTS:
            _type = MBS_SIGN_DOCUMENTS_OP_FACT
        self.hint = _hint(_type)
        self.token = iso8601TimeStamp()


class Operation(object):
    def __init__(self, hint, fact, memo, id):
        self.memo = memo
        self.id = id
        self.hint = _hint(hint)
        self.fact = fact
        self.factSigns = []
        self.hash = None

    def bytes(self):
        assert self.factSigns, 'Empty fact_signs'

        bFactHash = self.fact.hash.digest
        bMemo = self.memo.encode()

        bFactSigns = bytearray()
        for sg in self.factSigns:
            bFactSigns += bytearray(sg.bytes())
        bFactSign = bytes(bFactSigns)

        return concat(bFactHash, bFactSign, bMemo)

    def addFactSign(self, priv):
        factSign = newFactSign(self.fact.hash.digest, self.id, priv)
        self.factSigns.append(factSign)
        self.generateHash()

    def generateHash(self):
        self.hash = sha3(self.bytes())

    def dict(self):
        assert self.factSigns, 'Empty fact_signs'
        operation = {}
        operation['memo'] = self.memo
        operation['_hint'] = self.hint.hint
        operation['fact'] = self.fact.dict()
        operation['hash'] = self.hash.hash

        fact_signs = list()
        for _sg in self.factSigns:
            fact_signs.append(_sg.dict())
        operation['fact_signs'] = fact_signs

        return operation

    def json(self, file_name):
        assert self.factSigns, 'Empty fact_signs'
        with open(file_name, "w") as fp:
            json.dump(self.dict(), fp, indent=4)


class OperationGenerator(object):
    def __init__(self, id):
        self.id = id

    def setId(self, id):
        self.id = id
