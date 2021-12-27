import json

import base58
from mitumc.common import (Int, _hint, bconcat, iso8601TimeStamp, parseType,
                           parseISOtoUTC)
from mitumc.hash import sha
from mitumc.hint import (BASE_FACT_SIGN, KEY_PRIVATE, MC_ADDRESS, MC_AMOUNT)
from mitumc.key.keypair import getKeypairFromPrivateKey


def newFactSign(b, networkId, signKey):
    assert isinstance(b, bytes), 'Invalid target b; _newFactSign'
    _, type = parseType(signKey)
    assert type == KEY_PRIVATE, 'Invalid sign key; _newFactSign'

    kp = getKeypairFromPrivateKey(signKey)
    signature = kp.sign(bconcat(b, networkId.encode()))

    return FactSign(
        _hint(BASE_FACT_SIGN),
        kp.publicKey,
        signature,
        iso8601TimeStamp(),
    )

class Amount(object):
    def __init__(self, big, cid):
        self.hint = _hint(MC_AMOUNT)
        self.big = Int(big)
        self.cid = cid

    def bytes(self):
        bbig = self.big.tight()
        bcid = self.cid.encode()

        return bconcat(bbig, bcid)

    def dict(self):
        amount = {}
        amount['_hint'] = self.hint.hint
        amount['amount'] = str(self.big.value)
        amount['currency'] = self.cid
        return amount


class Address(object):

    def __init__(self, addr):
        _, type = parseType(addr)
        assert type == MC_ADDRESS, 'Invalid address; Address'
        self.addr = addr

    @property
    def address(self):
        return self.addr

    def bytes(self):
        return self.address.encode()


class FactSign(object):
    def __init__(self, signer, sign, signedAt):
        self.hint = _hint(BASE_FACT_SIGN)
        self.signer = signer
        self.sign = sign
        self.signedAt = signedAt

    def bytes(self):
        bsigner = self.signer.encode()
        bsign = self.sign
        btime = parseISOtoUTC(self.signedAt).encode()

        return bconcat(bsigner, bsign, btime)

    def dict(self):
        fact_sign = {}
        fact_sign['_hint'] = self.hint.hint
        fact_sign['signer'] = self.signer
        fact_sign['signature'] = base58.b58encode(self.sign).decode()
        fact_sign['signed_at'] = self.signedAt[:26] + 'Z'
        return fact_sign


# skeleton: CreateAccountsFact, KeyUpdaterFact, TransfersFact
class OperationFact(object):
    def __init__(self, hint):
        self.hint = _hint(hint)
        self.token = iso8601TimeStamp()


class Operation(object):
    def __init__(self, hint, fact, memo, networkId):
        self.memo = memo
        self.networkId = networkId
        self.hint = _hint(hint)
        self.fact = fact
        self.factSigns = []
        self.hash = None

    def bytes(self):
        assert self.factSigns, 'Empty fact_signs'

        bfactHash = self.fact.hash.digest
        bmemo = self.memo.encode()

        bfactSigns = bytearray()
        for sg in self.factSigns:
            bfactSigns += bytearray(sg.bytes())
        bfact_sg = bytes(bfactSigns)

        return bconcat(bfactHash, bfact_sg, bmemo)

    def addFactSign(self, priv):
        factSign = newFactSign(self.fact.hash.hash, self.networkId, priv)
        self.factSigns.append(factSign)
        self.generateHash()

    def generateHash(self):
        return sha.sha3(self.bytes())

    def dict(self):
        assert self.factSigns, 'Empty fact_signs'
        oper = {}
        oper['memo'] = self.memo
        oper['_hint'] = self.hint.hint
        oper['fact'] = self.fact.dict()
        oper['hash'] = self.hash.hash

        fact_signs = list()
        for _sg in self.factSigns:
            fact_signs.append(_sg.dict())
        oper['fact_signs'] = fact_signs

        return oper

    def json(self, file_name):
        assert self.factSigns, 'Empty fact_signs'
        with open(file_name, "w") as fp:
            json.dump(self.dict(), fp)
  
