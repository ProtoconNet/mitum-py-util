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
from mitumc.key.base import KeyPair, to_basekey


class BTCKeyPair(KeyPair):
    """ Contains BTC private key and its derived public key as a keypair.

    Attributes:
        privkey (BaseKey): BTC Private Key
        pubkey  (BaseKey): BTC Public Key
    """
    def __init__(self, priv, pub):
        super(BTCKeyPair, self).__init__(priv, pub)

    def sign(self, b):
        """ Returns raw BTC-ECDSA signature for binary input.

        Args:
            b (bytes): Target to sign

        Returns:
            bytes: Signature signed with privkey
        """
        assert isinstance(b, bytes), 'Input must be provided in byte format'

        setup('mainnet')
        
        hs = sha.sha256(b).digest
        wif = self.privkey.key
        
        pk = PrivateKey(wif=wif)
        sk = ecdsa.SigningKey.from_string(pk.key.to_string(), curve=SECP256k1)
        
        return sk.sign(hs, hashfunc=hashlib.sha256, sigencode=sigencode_der_canonize)


def to_btc_keypair(priv):
    """ Returns BTCKeyPair for provided private key.

    Args:
        priv (str): Hintless BTC private key
        
    Returns:
        BTCKeyPair: BTCKeyPair for priv
    """
    assert isinstance(priv, str), 'Key must be provided in string format'
    assert '-' not in priv, 'Key must be parsed before generating KeyPair'

    wif = base58.b58encode_check(base58.b58decode_check(priv)[:-1]).decode()
    wallet = Wallet(wif)
    pubk = base58.b58encode(codecs.decode(wallet.address.pubkeyc, "hex")).decode()

    return BTCKeyPair(
        to_basekey(BTC_PRIVKEY, wif),
        to_basekey(BTC_PBLCKEY, pubk)
    )
