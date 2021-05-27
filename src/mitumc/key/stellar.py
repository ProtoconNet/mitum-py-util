import stellar_sdk as stellar
from mitumc.hint import STELLAR_PBLCKEY, STELLAR_PRIVKEY
from mitumc.key.base import KeyPair, to_basekey


class StellarKeyPair(KeyPair):
    """ Contains Stellar private key and its derived public key as a keypair.

    Attributes:
        privkey (BaseKey): Stellar Private Key
        pubkey  (BaseKey): Stellar Public Key
    """
    def __init__(self, priv, pub):
        super(StellarKeyPair, self).__init__(priv, pub)

    def sign(self, b):
        """ Returns raw Stellar signature for binary input.

        Args:
            b (bytes): Target to sign

        Returns:
            bytes: Signature signed with privkey
        """
        assert isinstance(b, bytes), 'Input must be provided in byte format'

        kp = stellar.Keypair.from_secret(self.privkey.key)

        return kp.sign(b)


def to_stellar_keypair(priv):
    """ Returns StellarKeyPair for provided private key.

    Args:
        priv (str): Hintless Stellar private key
        
    Returns:
        StellarKeyPair: StellarKeyPair for priv
    """
    assert isinstance(priv, str), 'Key must be provided in string format'
    assert '-' not in priv, 'Key must be parsed before generating KeyPair'

    kp = stellar.Keypair.from_secret(priv)
    pubk = kp.public_key

    return StellarKeyPair(
        to_basekey(STELLAR_PRIVKEY, kp.secret),
        to_basekey(STELLAR_PBLCKEY, pubk))
