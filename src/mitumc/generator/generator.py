import base58

from ..hint import SEAL

from ..hash import sha3
from ..common import (
    iso8601TimeStamp, parseISOtoUTC, getNewToken, concatBytes, _hint)
from ..key import getKeypairFromPrivateKey

from ..operation import Operation
from ..operation.currency import CurrencyGenerator
from ..operation.document import DocumentGenerator


class Generator(object):
    def __init__(self, id):
        self.id = id
        self.currency = CurrencyGenerator(id)
        self.document = DocumentGenerator(id)

    def setId(self, id):
        self.id = id
        self.currency = CurrencyGenerator(id)
        self.document = DocumentGenerator(id)

    def getOperation(self, fact, memo):
        return Operation(fact, memo, self.id)

    def getSeal(self, signKey, operations):
        assert operations, 'Operation list is empty; Generator.getSeal'

        for op in operations:
            assert isinstance(op, Operation), 'Some objects in the operation list are not Operation; Generator.getSeal'
            assert op.hash != None, "Some operations in the operation list are not signed; Generator.getSeal"

        kp = getKeypairFromPrivateKey(signKey)

        signedAt = iso8601TimeStamp()
        bSignedAt = parseISOtoUTC(signedAt).encode()

        bSigner = kp.publicKey.encode()

        bopers = bytearray()
        for op in operations:
            bopers += op.hash.digest

        bodyHash = sha3(concatBytes(bSigner, bSignedAt, bopers))
        signature = kp.sign(concatBytes(bodyHash.digest, self.id.encode()))
        hash = sha3(concatBytes(bodyHash.digest, signature))

        seal = {}
        seal['_hint'] = _hint(SEAL).hint
        seal['hash'] = hash.hash
        seal['body_hash'] = bodyHash.hash
        seal['signer'] = kp.publicKey
        seal['signature'] = base58.b58encode(signature).decode()
        seal['signed_at'] = getNewToken(signedAt)

        _operations = list()
        for op in operations:
            _operations.append(op.dict())
        seal['operations'] = _operations

        return seal
