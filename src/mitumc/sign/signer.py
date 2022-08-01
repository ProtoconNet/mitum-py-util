import json
import base58

from .sign import newFactSign
from ..hash import sha3
from ..common import parseISOtoUTC, concatBytes


def _factSignToBuffer(fs):
    bSigner = fs['signer'].encode()
    bSign = base58.b58decode(fs['signature'].encode())
    bat = parseISOtoUTC(fs['signed_at']).encode()

    return concatBytes(bSigner, bSign, bat)


def _factSignsToBuffer(_factSigns):
    buffers = bytearray(''.encode())
    for _fs in _factSigns:
        buffers += bytearray(_factSignToBuffer(_fs))
    return buffers


class Signer(object):
    def __init__(self, id, signKey):
        self.id = id
        self.signKey = signKey

    def setId(self, id):
        self.id = id

    def signOperation(self, target):
        before = None
        if type(target) == type(""):
            with open(target) as jf:
                before = json.load(jf)
        elif type(target) == type({}):
            before = target

        if not before:
            return None

        after = {}
        factHash = before['fact']['hash']
        bFactHash = base58.b58decode(factHash.encode())
        factSign = before['fact_signs']

        factSign.append(
            newFactSign(
                bFactHash,
                self.id,
                self.signKey
            ).dict()
        )
        bFactSign = _factSignsToBuffer(factSign)

        after['memo'] = before['memo']
        after['_hint'] = before['_hint']
        after['fact'] = before['fact']
        after['fact_signs'] = factSign

        bMemo = before['memo'].encode()
        after['hash'] = base58.b58encode(
            sha3(
                concatBytes(bFactHash, bFactSign, bMemo)
            ).digest
        ).decode()
        return after
