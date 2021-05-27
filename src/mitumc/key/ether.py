import codecs
import hashlib

import ecdsa
from ecdsa import curves
from ecdsa.util import sigencode_der_canonize
from eth_keys import keys
from mitumc.common import Int, bconcat
from mitumc.hint import ETHER_PBLCKEY, ETHER_PRIVKEY
from mitumc.key.base import KeyPair, to_basekey


class ETHKeyPair(KeyPair):
    """ Contains ETH private key and its derived public key as a keypair.

    Attributes:
        privkey (BaseKey): ETH Private Key
        pubkey  (BaseKey): ETH Public Key
    """
    def __init__(self, priv, pub):
        super(ETHKeyPair, self).__init__(priv, pub)

    def sign(self, b):
        """ Returns raw ETH-ECDSA signature for binary input.

        Args:
            b (bytes): Target to sign

        Returns:
            bytes: Signature signed with privkey
        """
        assert isinstance(b, bytes), 'Input must be provided in byte format'

        pk = self.privkey.key
        sk = ecdsa.SigningKey.from_string(
            codecs.decode(pk, "hex"),
            curve=curves.SECP256k1,
            hashfunc=hashlib.sha256
        )

        sig = sk.sign(b, hashfunc=hashlib.sha256, sigencode=sigencode_der_canonize)

        rlen = Int(int(sig[3]))
        r = sig[4:4+rlen.value]
        s = sig[6+rlen.value:]

        return bconcat(rlen.little4_to_bytes(), r, s) 


def to_ether_keypair(priv):
    """ Returns ETHKeyPair for provided private key.

    Args:
        priv (str): Hintless BTC private key
        
    Returns:
        ETHKeyPair: ETHKeyPair for priv
    """
    assert isinstance(priv, str), 'Key must be provided in string format'
    assert '-' not in priv, 'Key must be parsed before generating KeyPair'

    pk = keys.PrivateKey(codecs.decode(priv, "hex"))
    pubk = pk.public_key.to_hex()[0] + '4' + pk.public_key.to_hex()[2:]

    return ETHKeyPair(
        to_basekey(ETHER_PRIVKEY, priv),
        to_basekey(ETHER_PBLCKEY, pubk),
    )
