import stellar_sdk as stellar
from mitum.hint import STELLAR_PBLCKEY, STELLAR_PRIVKEY
from mitum.key.base import BaseKey, KeyPair, to_basekey


class StellarKeyPair(KeyPair):
    fields = (
        ('privkey', BaseKey),
        ('pubkey', BaseKey),
    )

    def sign(self, b):
        kp = stellar.Keypair.from_secret(self.as_dict()['privkey'].key)

        return kp.sign(b)

    @property
    def public_key(self):
        return self.as_dict()['pubkey']


def new_stellar_keypair():
    kp = stellar.Keypair.random()

    return StellarKeyPair(
        to_basekey(STELLAR_PRIVKEY, kp.secret),
        to_basekey(STELLAR_PBLCKEY, kp.public_key))


def to_stellar_keypair(priv):
    kp = stellar.Keypair.from_secret(priv)
    pubk = kp.public_key

    return StellarKeyPair(
        to_basekey(STELLAR_PRIVKEY, kp.secret),
        to_basekey(STELLAR_PBLCKEY, pubk))
