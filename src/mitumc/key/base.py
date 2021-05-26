import rlp
from mitumc.common import Hash, Hint, Int, bconcat
from mitumc.constant import VERSION
from mitumc.hash import sha
from mitumc.hint import (BTC_PBLCKEY, BTC_PRIVKEY, ETHER_PBLCKEY,
                         ETHER_PRIVKEY, STELLAR_PBLCKEY, STELLAR_PRIVKEY)
from rlp.sedes import List, text


class BaseKey(rlp.Serializable):
    """ Contains a key and its type hint.

    Attributes:
        h (Hint): hint; [TYPE]_PBLCKEY, [TYPE]_PRIVKEY
        k (text): Hintless key
    """
    fields = (
        ('h', Hint),
        ('k', text),
    )

    @property
    def key(self):
        # Returns hintless key
        return self.as_dict()['k']

    def hint(self):
        return self.as_dict()['h']

    def hinted(self):
        # Returns hinted key
        return self.as_dict()['k'] + "-" + self.as_dict()['h'].hint

    def to_bytes(self): 
        # Returns hintless key in byte format
        return self.as_dict()['k'].encode()
    

class Key(rlp.Serializable):
    """ Single key with weight.
    
    Attributes:
        h    (Hint): hint; MC_KEY
        k (BaseKey): Basekey object for key
        w     (Int): weight
    """
    fields = (
        ('h', Hint),
        ('k', BaseKey),
        ('w', Int),
    )

    def key_bytes(self):
        # Returns hintless key in byte format
        return self.as_dict()['k'].to_bytes()

    def to_bytes(self):
        # Returns concatenated [key, weight] in byte format
        d = self.as_dict()
        bkey = d['k'].hinted().encode()
        bweight = self.as_dict()['w'].to_bytes()

        return bconcat(bkey, bweight)

    def to_dict(self):
        d = self.as_dict()
        key = {}
        key['_hint'] = d['h'].hint
        key['weight'] = d['w'].value
        key['key'] = d['k'].hinted()
        return key


class KeysBody(rlp.Serializable):
    """ Body of Keys.

    Attributes:
        h              (Hint): hint; MC_KEYS
        threshold       (Int): threshold
        ks        (List(Key)): List of keys
    """
    fields = (
        ('h', Hint),
        ('threshold', Int),
        ('ks', List((Key,), False)),
    )

    def to_bytes(self):
        # Returns concatenated [ks, threshold] in byte format
        d = self.as_dict()
        keys = d['ks']

        lkeys = list(keys)
        lkeys.sort(key=lambda x: x.key_bytes())

        bkeys = bytearray()
        for k in lkeys:
            bkeys += k.to_bytes()

        bkeys = bytes(bkeys)
        bthreshold = d['threshold'].to_bytes()

        return bconcat(bkeys, bthreshold)

    def generate_hash(self):
        return sha.sum256(self.to_bytes())


class Keys(rlp.Serializable):
    """ Contains KeysBody and a hash.

    Attributes:
        hs       (Hash): Keys Hash
        body (KeysBody): Body object
    """
    fields = (
        ('hs', Hash),
        ('body', KeysBody),
    )

    def to_bytes(self):
        return self.as_dict()['body'].to_bytes()

    def hash(self):
        return self.as_dict()['hs']

    def to_dict(self):
        d = self.as_dict()['body'].as_dict()
        keys = {}
        keys['_hint'] = d['h'].hint
        keys['hash'] = self.hash().hash

        _keys = d['ks']
        ks = list()
        for _key in _keys:
            ks.append(_key.to_dict())
        keys['keys'] = ks
        keys['threshold'] = d['threshold'].value
        return keys


# skeleton
class KeyPair(rlp.Serializable):
    fields = (
        ('privkey', BaseKey),
        ('pubkey', BaseKey),
    )

    def sign(self):
        pass


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
