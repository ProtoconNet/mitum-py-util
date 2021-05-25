import codecs
import hashlib

import ecdsa
from ecdsa import curves
from ecdsa.util import sigencode_der_canonize
from eth_keys import keys
from mitumc.common import Int, bconcat
from mitumc.hint import ETHER_PBLCKEY, ETHER_PRIVKEY
from mitumc.key.base import BaseKey, KeyPair, to_basekey


class ETHKeyPair(KeyPair):
    fields = (
        ('privkey', BaseKey),
        ('pubkey', BaseKey),
    )

    def sign(self, b):
        pk = self.as_dict()['privkey'].key
        sk = ecdsa.SigningKey.from_string(
            codecs.decode(pk, "hex"),
            curve=curves.SECP256k1,
            hashfunc=hashlib.sha256
        )

        sig = sk.sign(b, hashfunc=hashlib.sha256, sigencode=sigencode_der_canonize)

        rlen = Int(int(sig[3]))
        r = sig[4:4+rlen.value]
        s = sig[6+rlen.value:]

        signature = bconcat(rlen.little4_to_bytes(), r, s)

        return signature

    @property
    def public_key(self):
        return self.as_dict()['pubkey']


def to_ether_keypair(priv):
    pk = keys.PrivateKey(codecs.decode(priv, "hex"))
    pubk = pk.public_key.to_hex()[0] + '4' + pk.public_key.to_hex()[2:]

    return ETHKeyPair(
        to_basekey(ETHER_PRIVKEY, priv),
        to_basekey(ETHER_PBLCKEY, pubk),
    )
