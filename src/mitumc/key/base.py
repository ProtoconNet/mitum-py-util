from mitumc.common import Hint, bconcat
from mitumc.constant import VERSION
from mitumc.hash import sha
from mitumc.hint import (BTC_PBLCKEY, BTC_PRIVKEY, ETHER_PBLCKEY,
                         ETHER_PRIVKEY, STELLAR_PBLCKEY, STELLAR_PRIVKEY)


class BaseKey(object):
    """ Contains a key and its type hint.

    Attributes:
        h (Hint): hint; [TYPE]_PBLCKEY, [TYPE]_PRIVKEY
        k (str): Hintless key
    """

    def __init__(self, h, k):
        self.h = h
        self.k = k

    @property
    def key(self):
        # Returns hintless key
        return self.k

    def hint(self):
        return self.h

    def hinted(self):
        # Returns hinted key
        return self.k + "-" + self.h.hint

    def to_bytes(self): 
        # Returns hintless key in byte format
        return self.k.encode()
    

class Key(object):
    """ Single key with weight.
    
    Attributes:
        h    (Hint): hint; MC_KEY
        k (BaseKey): Basekey object for key
        w     (Int): weight
    """
    def __init__(self, h, k, w):
        self.h = h
        self.k = k
        self.w = w

    def key_bytes(self):
        # Returns hintless key in byte format
        return self.k.to_bytes()

    def to_bytes(self):
        # Returns concatenated [key, weight] in byte format
        bkey = self.k.hinted().encode()
        bweight = self.w.to_bytes()

        return bconcat(bkey, bweight)

    def to_dict(self):
        key = {}
        key['_hint'] = self.h.hint
        key['weight'] = self.w.value
        key['key'] = self.k.hinted()
        return key


class KeysBody(object):
    """ Body of Keys.

    Attributes:
        h              (Hint): hint; MC_KEYS
        threshold       (Int): threshold
        ks        (List(Key)): List of keys
    """
    def __init__(self, h, threshold, ks):
        self.h = h
        self.threshold = threshold
        self.ks = ks

    def to_bytes(self):
        # Returns concatenated [ks, threshold] in byte format
        keys = self.ks

        lkeys = list(keys)
        lkeys.sort(key=lambda x: x.key_bytes())

        bkeys = bytearray()
        for k in lkeys:
            bkeys += k.to_bytes()

        bkeys = bytes(bkeys)
        bthreshold = self.threshold.to_bytes()

        return bconcat(bkeys, bthreshold)

    def generate_hash(self):
        return sha.sum256(self.to_bytes())


class Keys(object):
    """ Contains KeysBody and a hash.

    Attributes:
        hs       (Hash): Keys Hash
        body (KeysBody): Body object
    """
    def __init__(self, hs, body):
        self.hs = hs
        self.body = body

    def to_bytes(self):
        return self.body.to_bytes()

    def hash(self):
        return self.hs

    def to_dict(self):
        d = self.body
        keys = {}
        keys['_hint'] = d.h.hint
        keys['hash'] = self.hash().hash

        _keys = d.ks
        ks = list()
        for _key in _keys:
            ks.append(_key.to_dict())
        keys['keys'] = ks
        keys['threshold'] = d.threshold.value
        return keys


# skeleton
class KeyPair(object):
    def __init__(self, priv, pub):
        self.privkey = priv
        self.pubkey = pub

    @property
    def private_key(self):
        return self.privkey

    @property
    def public_key(self):
        return self.pubkey


def to_basekey(type, k):
    """ Returns BaseKey for k

    Args:
        type (str): Type hint for key
        k    (str): Hintless key

    Returns:
        BaseKey: BaseKey object for k
    """
    assert type in [
        BTC_PRIVKEY, BTC_PBLCKEY,
        ETHER_PRIVKEY, ETHER_PBLCKEY,
        STELLAR_PRIVKEY, STELLAR_PBLCKEY], '[arg1] Invalid type or not a key type'
    assert isinstance(k, str), '[arg2] Key must be provided in string format'
    
    hint = Hint(type, VERSION)
    return BaseKey(hint, k)
