import base58

from ..hash import sha3
from ..common import (
    iso8601TimeStamp, parseISOtoUTC, getNewToken, concatBytes, _hint)
from ..key import getKeypairFromPrivateKey

from ..operation import Operation
from ..operation.blockcity import BlockCityGenerator
from ..operation.currency import CurrencyGenerator
from ..operation.blocksign import BlockSignGenerator
from ..hint import (MBC_CREATE_DOCUMENTS_OP, MBC_CREATE_DOCUMENTS_OP_FACT, MBC_UPDATE_DOCUMENTS_OP, MBC_UPDATE_DOCUMENTS_OP_FACT, MC_CREATE_ACCOUNTS_OP_FACT, 
                         MC_CREATE_ACCOUNTS_OP, MC_KEYUPDATER_OP_FACT, MC_KEYUPDATER_OP, MC_TRANSFERS_OP_FACT, MC_TRANSFERS_OP, 
                         MBS_CREATE_DOCUMENTS_OP_FACT, MBS_CREATE_DOCUMENTS_OP, MBS_SIGN_DOCUMENTS_OP_FACT, MBS_SIGN_DOCUMENTS_OP, SEAL)


class Generator(object):
    def __init__(self, id):
        self.id = id
        self.currency = CurrencyGenerator(id)
        self.blockSign = BlockSignGenerator(id)
        self.blockCity = BlockCityGenerator(id)

    def setId(self, id):
        self.id = id
        self.currency = CurrencyGenerator(id)
        self.blockSign = BlockSignGenerator(id)
        self.blockCity = BlockCityGenerator(id)

    def createOperation(self, fact, memo):

        if fact.hint.type == MC_CREATE_ACCOUNTS_OP_FACT:
            _type = MC_CREATE_ACCOUNTS_OP
        elif fact.hint.type == MC_KEYUPDATER_OP_FACT:
            _type = MC_KEYUPDATER_OP
        elif fact.hint.type == MC_TRANSFERS_OP_FACT:
            _type = MC_TRANSFERS_OP
        elif fact.hint.type == MBS_CREATE_DOCUMENTS_OP_FACT:
            _type = MBS_CREATE_DOCUMENTS_OP
        elif fact.hint.type == MBS_SIGN_DOCUMENTS_OP_FACT:
            _type = MBS_SIGN_DOCUMENTS_OP
        elif fact.hint.type == MBC_CREATE_DOCUMENTS_OP_FACT:
            _type = MBC_CREATE_DOCUMENTS_OP
        elif fact.hint.type == MBC_UPDATE_DOCUMENTS_OP_FACT:
            _type = MBC_UPDATE_DOCUMENTS_OP
        else:
            return None

        return Operation(_type, fact, memo, self.id)

    def createSeal(self, signKey, operations):
        assert operations, 'Operation list is empty!'

        for op in operations:
            assert isinstance(op, Operation), 'Not Operation; createSeal'
            assert op.hash != None, "Operation haven't signed; createSeal"

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
