import json

from ..common import (_hint, concatBytes, iso8601TimeStamp)
from ..hash import sha3
from ..sign import newFactSign


class OperationFact(object):
    def __init__(self, hint):
        self.hint = _hint(hint)
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

        return concatBytes(bFactHash, bFactSign, bMemo)

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
