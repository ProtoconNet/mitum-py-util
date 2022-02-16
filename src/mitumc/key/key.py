from ..common import concatBytes, parseType, _hint, Int
from ..hash import sha3
from ..hint import (KEY_PUBLIC, MC_ADDRESS, MC_KEY, MC_KEYS)

from .base import BaseKey


class Key(object):
    def __init__(self, key, weight):
        raw, type = parseType(key)
        assert type == KEY_PUBLIC, 'Not public key; Key'
        assert weight > 0 and weight <= 100, "Weight should be in range 0 < weight <= 100; Key"

        self.hint = _hint(MC_KEY)
        self.key = BaseKey(KEY_PUBLIC, raw)
        self.weight = Int(weight)

    def bytesKey(self):
        return self.key.bytesWithoutType()

    def bytes(self):
        bKey = self.key.bytes()
        bWeight = self.weight.bytes()

        return concatBytes(bKey, bWeight)

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
        self.hash = sha3(self.bytes())

    def bytes(self):
        keys = self.keys

        listKeys = list(keys)
        listKeys.sort(key=lambda x: x.bytesKey())

        bKeys = bytearray()
        for k in listKeys:
            bKeys += k.bytes()

        bKeys = bytes(bKeys)
        bThreshold = self.threshold.bytes()

        return concatBytes(bKeys, bThreshold)

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


class Address(object):
    def __init__(self, addr):
        _, type = parseType(addr)
        assert type == MC_ADDRESS, 'Invalid address; Address'
        self.addr = addr

    @property
    def address(self):
        return self.addr

    def bytes(self):
        return self.address.encode()
