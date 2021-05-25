import base58
import rlp
from mitum.common import (Hash, Hint, Int, bconcat, iso8601TimeStamp,
                          parseAddress, parseISOtoUTC)
from mitum.constant import VERSION
from mitum.hint import (BASE_FACT_SIGN, BTC_PRIVKEY, ETHER_PRIVKEY,
                        STELLAR_PRIVKEY)
from mitum.key.base import BaseKey
from mitum.key.btc import to_btc_keypair
from mitum.key.ether import to_ether_keypair
from mitum.key.stellar import to_stellar_keypair
from rlp.sedes import List, binary, text


def _newFactSign(b, hinted_priv):
    stype, saddr = parseAddress(hinted_priv)
        
    signature = None

    if stype == BTC_PRIVKEY:
        kp = to_btc_keypair(saddr)
        signature = kp.sign(b)
    elif stype == ETHER_PRIVKEY:
        kp = to_ether_keypair(saddr)
        signature = kp.sign(b)
    elif stype == STELLAR_PRIVKEY:
        kp = to_stellar_keypair(saddr)
        signature = kp.sign(bconcat(b))

    vk = kp.public_key

    return FactSign(
        Hint(BASE_FACT_SIGN, VERSION),
        vk,
        signature,
        iso8601TimeStamp(),
    )


class Memo(rlp.Serializable):
    fields = (
        ('m', text),
    )
    
    @property
    def memo(self):
        return self.as_dict()['m']
    
    def to_bytes(self):
        return self.as_dict()['m'].encode()


class Amount(rlp.Serializable):
    fields = (
        ('h', Hint),
        ('big', Int),
        ('cid', text),
    )

    def to_bytes(self):
        d = self.as_dict()
        bbig = d['big'].tight_bytes()
        bcid = d['cid'].encode()

        return bconcat(bbig, bcid)

    def to_dict(self):
        d = self.as_dict()
        amount = {}
        amount['_hint'] = d['h'].hint
        amount['amount'] = str(d['big'].value)
        amount['currency'] = d['cid']
        return amount


class Address(rlp.Serializable):
    fields = (
        ('h', Hint),
        ('addr', text),
    )

    def hint(self):
        return self.as_dict()['h'].hint

    def hinted(self):
        d = self.as_dict()
        return d['addr'] + '-' + d['h'].hint

    def to_bytes(self):
        return self.as_dict()['addr'].encode()


class FactSign(rlp.Serializable):
    fields = (
            ('h', Hint),
            ('signer', BaseKey),
            ('sign', binary),
            ('t', text),
        )

    def to_bytes(self):
        d = self.as_dict()
        bsigner = d['signer'].hinted().encode()
        bsign = d['sign']
        btime = parseISOtoUTC(d['t']).encode()

        return bconcat(bsigner, bsign, btime)

    def signed_at(self):
       return self.as_dict()['t'][:26] + 'Z'

    def to_dict(self):
        d = self.as_dict()
        fact_sign = {}
        fact_sign['_hint'] = d['h'].hint
        fact_sign['signer'] = d['signer'].hinted()
        fact_sign['signature'] = base58.b58encode(d['sign']).decode()
        fact_sign['signed_at'] = self.signed_at()
        return fact_sign


class OperationFactBody(rlp.Serializable):
    fields = (
        ('h', Hint),
        ('token', text),
    )

    def to_bytes(self):
        pass

    def generate_hash(self):
        pass


class OperationFact(rlp.Serializable):
    fields = (
        ('hs', Hash),
        ('body', OperationFactBody),
    )

    def hash(self):
        return self.as_dict()['hs']

    def newFactSign(self, net_id, hinted_priv):
        b = bconcat(self.hash().digest, net_id.encode())
        return _newFactSign(b, hinted_priv)
    
    def to_dict(self):
        pass


class OperationBody(rlp.Serializable):
    fields = (
        ('h', Hint),
        ('fact', OperationFact),
        ('fact_sg', List((FactSign,), False)),
    )

    def generate_hash(self):
        pass


class Operation(rlp.Serializable):
    fields = (
        ('hs', Hash),
        ('body', OperationBody),
    )

    def hash(self):
        return self.as_dict()['hs']

    def to_dict(self):
        pass
