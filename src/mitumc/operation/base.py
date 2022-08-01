import base64
import json

from ..key import Address
from ..common import MitumFactor, _hint, concatBytes, iso8601TimeStamp
from ..hash import sha3
from ..sign import newFactSign


class Item(MitumFactor):
    def __init__(self, itemType):
        self.hint = _hint(itemType)
        

class OperationFact(MitumFactor):
    def __init__(self, hint):
        self.hint = _hint(hint)
        self.token = iso8601TimeStamp()
        
    @property
    def operationHint(self):
        assert False, 'Unimplemented function operationHint; OperationFact'

    def generateHash(self):
        self.hash = sha3(self.bytes())


class GeneralOperationFact(OperationFact):
    def __init__(self, factType, sender, items):
        super(GeneralOperationFact, self).__init__(factType)
        self.sender = Address(sender)
        self.items = items
        self.generateHash()

    def bytes(self):
        bitems = bytearray()
        for i in self.items:
            bitems += bytearray(i.bytes())

        bToken = self.token.encode()
        bSender = self.sender.bytes()
        bitems = bytes(bitems)

        return concatBytes(bToken, bSender, bitems)

    def dict(self):
        fact = {}
        fact['_hint'] = self.hint.hint
        fact['hash'] = self.hash.hash
        token = base64.b64encode(self.token.encode('ascii')).decode('ascii')
        fact['token'] = token
        fact['sender'] = self.sender.address

        _items = list()
        for item in self.items:
            _items.append(item.dict())
        fact['items'] = _items
        
        return fact    


class PurposedOperationFact(OperationFact):
    pass


class Operation(MitumFactor):
    def __init__(self, fact, memo, id):
        self.memo = memo
        self.id = id
        self.hint = fact.operationHint
        self.fact = fact
        self.factSigns = []
        self.hash = None

    def bytes(self):
        assert self.factSigns, 'Empty fact_signs; Operation.bytes'

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
        assert self.factSigns, 'Empty fact_signs; Operation.dict'
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
        assert self.factSigns, 'Empty fact_signs; Operation.json'
        with open(file_name, "w") as fp:
            json.dump(self.dict(), fp, indent=4)


class OperationGenerator(object):
    def __init__(self, id):
        self.id = id

    def setId(self, id):
        self.id = id
