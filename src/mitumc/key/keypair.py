import codecs
import hashlib

import base58

from bitcoinaddress.util import checksum
from bitcoinaddress import Wallet

from bitcoinutils.keys import PrivateKey
from bitcoinutils.setup import setup

import ecdsa
from ecdsa.curves import SECP256k1
from ecdsa.util import sigencode_der_canonize

from mitumc.hash import sha256, sha3
from mitumc.hint import KEY_PRIVATE, KEY_PUBLIC
from mitumc.key.base import BaseKey
from mitumc.common import parseType


class Keypair:
    def __init__(self, priv, useSeed):
        if not useSeed:
            raw, _ = parseType(priv)
            self.priv = BaseKey(KEY_PRIVATE, raw)
            self.seed = None
        else:
            self.priv = None
            self.seed = priv
        self.generatePrivateKey()
        self.generatePublicKey()

    def generatePrivateKey(self):
        if self.priv != None:
            assert isinstance(
                self.priv, BaseKey), 'Wrong private key or seed; Keypair'
        elif self.seed != None:
            assert len(
                self.seed) >= 36, 'Seed is too short to create Keypair; Keypair'
            sh = sha3(self.seed.encode())
            shb = base58.b58encode(sh.digest)[:-4]
            k = str(hex((int.from_bytes(shb, "big") % (SECP256k1.order - 1)) + 1))[2:]
            self.priv = BaseKey(KEY_PRIVATE, encodeKey(bytes.fromhex(k)))

    def generatePublicKey(self):
        wif = base58.b58encode_check(
            base58.b58decode_check(self.priv.key)[:-1]).decode()
        wallet = Wallet(wif)
        self.pub = BaseKey(KEY_PUBLIC, base58.b58encode(codecs.decode(
            wallet.address.pubkeyc, "hex")).decode())

    @property
    def privateKey(self):
        return self.priv.typed

    @property
    def publicKey(self):
        return self.pub.typed

    def sign(self, b):
        assert isinstance(b, bytes), 'Input must be provided in byte format'
        setup('mainnet')

        hs = sha256(b).digest
        wif = self.priv.key

        pk = PrivateKey(wif=wif)
        sk = ecdsa.SigningKey.from_string(pk.key.to_string(), curve=SECP256k1)

        return sk.sign(hs, hashfunc=hashlib.sha256, sigencode=sigencode_der_canonize)


def encodeKey(key):
    pk = b'\x80' + key + b'\x01'
    return base58.b58encode(pk + checksum(pk)).decode()


def getNewKeypair():
    return getKeypairFromPrivateKey(encodeKey(Wallet().key.digest) + KEY_PRIVATE)


def getKeypairFromPrivateKey(priv):
    _, type = parseType(priv)
    assert type == KEY_PRIVATE, 'Not private key; getKeypairFromPrivateKey'
    return Keypair(priv, False)


def getKeypairFromSeed(seed):
    assert len(
        seed) >= 36, 'Seed is too short to create Keypair; getKeypairFromseed'
    return Keypair(seed, True)
