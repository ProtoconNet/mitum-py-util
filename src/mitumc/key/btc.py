import codecs
import hashlib

import base58
import ecdsa
from bitcoinaddress import Wallet
from bitcoinutils.keys import PrivateKey
from bitcoinutils.setup import setup
from ecdsa.curves import SECP256k1
from ecdsa.util import sigencode_der_canonize
from mitumc.hash import sha
from mitumc.hint import BTC_PBLCKEY, BTC_PRIVKEY
from mitumc.key.base import BaseKey, KeyPair, to_basekey


class BTCKeyPair(KeyPair):
    fields = (
        ('privkey', BaseKey),
        ('pubkey', BaseKey),
    )

    def sign(self, b):
        setup('mainnet')
        
        hs = sha.sha256(b).digest
        wif = self.as_dict()['privkey'].key
        
        pk = PrivateKey(wif=wif)
        sk = ecdsa.SigningKey.from_string(pk.key.to_string(), curve=SECP256k1)
        
        signature = sk.sign(hs, hashfunc=hashlib.sha256, sigencode=sigencode_der_canonize)
        
        return signature

    @property
    def public_key(self):
        return self.as_dict()['pubkey']


def to_btc_keypair(priv):

    wif = base58.b58encode_check(base58.b58decode_check(priv)[:-1]).decode()
    wallet = Wallet(wif)
    pubk = base58.b58encode(codecs.decode(wallet.address.pubkeyc, "hex")).decode()

    return BTCKeyPair(
        to_basekey(BTC_PRIVKEY, wif),
        to_basekey(BTC_PBLCKEY, pubk)
    )
