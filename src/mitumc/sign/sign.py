import base58

from mitumc.key import getKeypairFromPrivateKey
from mitumc.key.hint import KEY_PRIVATE
from mitumc.common import parseType, iso8601TimeStamp, _hint, parseISOtoUTC, concat

from mitumc.sign.hint import BASE_FACT_SIGN


def newFactSign(b, id, signKey):
    assert isinstance(b, bytes), 'Invalid target b; newFactSign'
    _, type = parseType(signKey)
    assert type == KEY_PRIVATE, 'Invalid sign key; newFactSign'

    kp = getKeypairFromPrivateKey(signKey)
    signature = kp.sign(concat(b, id.encode()))

    return FactSign(
        kp.publicKey,
        signature,
        iso8601TimeStamp(),
    )


class FactSign(object):
    def __init__(self, signer, sign, signedAt):
        self.hint = _hint(BASE_FACT_SIGN)
        self.signer = signer
        self.sign = sign
        self.signedAt = signedAt

    def bytes(self):
        bSigner = self.signer.encode()
        bSign = self.sign
        bTime = parseISOtoUTC(self.signedAt).encode()

        return concat(bSigner, bSign, bTime)

    def dict(self):
        fact_sign = {}
        fact_sign['_hint'] = self.hint.hint
        fact_sign['signer'] = self.signer
        fact_sign['signature'] = base58.b58encode(self.sign).decode()
        fact_sign['signed_at'] = self.signedAt[:26] + 'Z'
        return fact_sign
