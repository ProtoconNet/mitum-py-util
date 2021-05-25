import rlp
from mitumc.common import Hash, Hint, Int, bconcat
from mitumc.constant import VERSION
from mitumc.hash import sha
from rlp.sedes import List, text


class BaseKey(rlp.Serializable):
    fields = (
        ('h', Hint),
        ('k', text),
    )

    @property
    def key(self):
        return self.as_dict()['k']

    def hint(self):
        return self.as_dict()['h']

    def hinted(self):
        return self.as_dict()['k'] + "-" + self.as_dict()['h'].hint

    def to_bytes(self):
        return self.as_dict()['k'].encode()
    

class Key(rlp.Serializable):
    fields = (
        ('h', Hint),
        ('k', BaseKey),
        ('w', Int),
    )

    def key_bytes(self):
        return self.as_dict()['k'].to_bytes()

    def to_bytes(self):
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
    fields = (
        ('h', Hint),
        ('threshold', Int),
        ('ks', List((Key,), False)),
    )

    def to_bytes(self):
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


class KeyPair(rlp.Serializable):
    fields = (
        ('privkey', BaseKey),
        ('pubkey', BaseKey),
    )

    def sign(self):
        pass


def to_basekey(type, k):
    hint = Hint(type, VERSION)
    return BaseKey(hint, k)
