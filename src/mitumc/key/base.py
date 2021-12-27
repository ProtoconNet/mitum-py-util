from mitumc.common import bconcat, parseType, _hint, Int
from mitumc.hash import sha
from mitumc.hint import (KEY_PUBLIC, MC_ADDRESS, MC_KEY, MC_KEYS)


class BaseKey(object):

    def __init__(self, type, key):
        self.type = type
        self.key = key

    @property
    def typed(self):
        return self.key + self.type

    def bytesWithoutType(self):
        return self.key.encode()

    def bytes(self):
        return self.typed.encode()


class Key(object):
    def __init__(self, key, weight):
        raw, type = parseType(key)
        assert type == KEY_PUBLIC, 'Not public key; Key'
        assert weight > 0 and weight <= 100, "Weight should be in range 0 < weight <= 100; Key"

        self.hint = _hint(MC_KEY)
        self.key = BaseKey(KEY_PUBLIC, raw)
        self.weight = Int(weight)

    def bytesKey(self):
        # Returns hintless key in byte format
        return self.key.bytesWithoutType()

    def bytes(self):
        # Returns concatenated [key, weight] in byte format
        bkey = self.key.bytes()
        bweight = self.weight.bytes()

        return bconcat(bkey, bweight)

    def dict(self):
        key = {}
        key['_hint'] = self.hint.hint
        key['weight'] = self.weight.value
        key['key'] = self.key.typed
        return key


class Keys(object):
    def __init__(self, keys, threshold):
        self.hint = _hint(MC_KEYS)
        self.threshold = Int(threshold)
        self.keys = keys
        self.hash = sha.sha3(self.bytes())

    def bytes(self):
            # Returns concatenated [ks, threshold] in byte format
        keys = self.keys

        lkeys = list(keys)
        lkeys.sort(key=lambda x: x.bytesKey())

        bkeys = bytearray()
        for k in lkeys:
            bkeys += k.bytes()

        bkeys = bytes(bkeys)
        bthreshold = self.threshold.bytes()

        return bconcat(bkeys, bthreshold)

    @property
    def address(self):
        return self.hash.hash + MC_ADDRESS

    def dict(self):
        keys = {}
        keys['_hint'] = self.hint.hint
        keys['hash'] = self.hash.hash

        _keys = self.keys
        ks = list()
        for _key in _keys:
            ks.append(_key.dict())
        keys['keys'] = ks
        keys['threshold'] = self.threshold.value
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