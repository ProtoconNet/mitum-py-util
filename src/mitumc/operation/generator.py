import json

import base58
from mitumc.common import (_hint, bconcat, getNewToken, iso8601TimeStamp, parseISOtoUTC)
from mitumc.hash import sha
from mitumc.hint import (MBS_CREATE_DOCUMENTS_OP, MBS_SIGN_DOCUMENTS_OP, MBS_TRANSFER_DOCUMENTS_OP,
                         MC_CREATE_ACCOUNTS_OP, MC_CREATE_ACCOUNTS_OP_FACT,
                         MC_KEYUPDATER_OP, MC_KEYUPDATER_OP_FACT, 
                         MC_TRANSFERS_OP, MC_TRANSFERS_OP_FACT, SEAL,
                         MBS_CREATE_DOCUMENTS_OP_FACT, MBS_CREATE_DOCUMENTS_OP,
                         MBS_SIGN_DOCUMENTS_OP_FACT, MBS_SIGN_DOCUMENTS_OP,
                         MBS_TRANSFER_DOCUMENTS_OP_FACT, MBS_TRANSFER_DOCUMENTS_OP)
from mitumc.key.base import Key, Keys
from mitumc.key.keypair import getKeypairFromPrivateKey
from mitumc.operation.base import Amount, Operation, Operation, newFactSign
from mitumc.operation.create_accounts import CreateAccountsFact, CreateAccountsItem
from mitumc.operation.key_updater import KeyUpdaterFact
from mitumc.operation.transfers import TransfersFact, TransfersItem
from mitumc.operation.create_documents import CreateDocumentsItem, CreateDocumentsFact
from mitumc.operation.transfer_document import TransferDocumentsItem, TransferDocumentsFact
from mitumc.operation.sign_document import SignDocumentsItem, SignDocumentsFact


def _to_keys(keys, threshold):
    _keys = []

    for _key in keys:
        key, weight = _key
        _keys.append(
            Key(key, weight)
        )

    keys = Keys(
        _keys,
        threshold,
    )

    return keys


def _to_amounts(amts):
    amounts = []

    for _amt in amts:
        amounts.append(
            Amount(
                _amt[0],
                _amt[1]
            )
        )

    return amounts


class Generator(object):
    def __init__(self, networkId):
        self.networkId = networkId

    def set_id(self, _id):
        self.networkId = _id

    def key(key, weight):
        return (key, weight)

    def amount(big, cid):
        return (big, cid)

    def createKeys(keys, threshold):
        return _to_keys(keys, threshold)

    def createAmounts(amts):
        return _to_amounts(amts)

    def createCreateAccountsItem(keys, amounts):
        return CreateAccountsItem(keys, amounts)

    def createTransfersItem(receiver, amounts):
        return TransfersItem(receiver, amounts)

    def createCreateDocumentsItem(filehash, did, signcode, title, size, cid, signers, signcodes):
        return CreateDocumentsItem(filehash, did, signcode, title, size, cid, signers, signcodes)

    def createSignDocumentsItem(owner, did, cid):
        return SignDocumentsItem(owner, did, cid)

    def createTransferDocumentsItem(owner, receiver, did, cid):
        return TransferDocumentsItem(owner, receiver, did, cid)

    def createCreateAccountsFact(sender, items):
        return CreateAccountsFact(sender, items)

    def createKeyUpdaterFact(target, keys, cid):
        return KeyUpdaterFact(target, keys, cid)

    def createTransfersFact(sender, items):
        return TransfersFact(sender, items)

    def createCreateDocumentsFact(sender, items):
        return CreateDocumentsFact(sender, items)

    def createSignDocumentsFact(sender, items):
        return SignDocumentsFact(sender, items)

    def createTransferDocumentsFact(sender, items):
        return TransferDocumentsFact(sender, items)

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
        elif fact.hint.type == MBS_TRANSFER_DOCUMENTS_OP_FACT:
            _type = MBS_TRANSFER_DOCUMENTS_OP
        else:
            return None

        return Operation(_type, fact, memo, self.networkId)

    def createSeal(self, signKey, operations):
        assert operations, 'Operation list is empty!'

        for op in operations:
            assert isinstance(op, Operation), 'Not Operation; createSeal'
            assert op.hash != None, "Operation haven't signed; createSeal"

        kp = getKeypairFromPrivateKey(signKey)

        signedAt = iso8601TimeStamp()
        bsignedAt = parseISOtoUTC(signedAt).encode()

        bsigner = kp.publicKey.encode()

        bopers = bytearray()
        for op in operations:
            bopers += op.hash.digest

        bodyHash = sha.sha3(bconcat(bsigner, bsignedAt, bopers))
        signature = kp.sign(bconcat(bodyHash.digest, self.networkId.encode()))
        hash = sha.sha3(bconcat(bodyHash.digest, signature))

        seal = {}
        seal['_hint'] = _hint(SEAL).hint
        seal['hash'] = hash.hash
        seal['body_hash'] = bodyHash.hash
        seal['signer'] = kp.publicKey
        seal['signature'] = base58.b58encode(signature).decode()
        seal['signed_at'] = getNewToken(signedAt)

        operations = list()
        for op in operations:
            operations.append(op.dict())
        seal['operations'] = operations

        return seal


class JSONParser(object):
    def toJSONString(seal):
        return json.dumps(seal)

    def generateFile(seal, fname):
        with open(fname, 'w') as fp:
            json.dump(seal, fp)


def _factSignToBuffer(fs):
    bsigner = fs['signer'].encode()
    bsign = base58.b58decode(fs['signature'].encode())
    bat = parseISOtoUTC(fs['signed_at']).encode()

    return bconcat(bsigner, bsign, bat)


def _factSignsToBuffer(_fact_signs):
    buffers = bytearray(''.encode())
    for _fs in _fact_signs:
        buffers += bytearray(_factSignToBuffer(_fs))
    return buffers


class Signer(object):
    def __init__(self, networkId, signKey):
        self.networkId = networkId
        self.signKey = signKey

    def setNetId(self, _id):
        self.networkId = _id

    def signOperation(self, f_oper):
        before = None
        if type(f_oper) == type(""):
            with open(f_oper) as jf:
                before = json.load(jf)
        elif type(f_oper) == type({}):
            before = f_oper

        if not before:
            return None

        after = {}
        fact_hash = before['fact']['hash']
        bfact_hash = base58.b58decode(fact_hash.encode())
        fact_sign = before['fact_signs']

        fact_sign.append(
            newFactSign(
                bfact_hash,
                self.networkId,
                self.signKey
            ).dict()
        )
        bfact_sg = _factSignsToBuffer(fact_sign)

        after['memo'] = before['memo']
        after['_hint'] = before['_hint']
        after['fact'] = before['fact']
        after['fact_signs'] = fact_sign

        bmemo = before['memo'].encode()
        after['hash'] = base58.b58encode(
            sha.sha3(
                bconcat(bfact_hash, bfact_sg, bmemo)
            ).digest
        ).decode()
        return after
