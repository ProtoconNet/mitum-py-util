import base58
import rlp
from mitumc.common import (Hash, Hint, Int, bconcat, iso8601TimeStamp,
                           parseAddress, parseISOtoUTC)
from mitumc.constant import VERSION
from mitumc.hint import (BASE_FACT_SIGN, BTC_PRIVKEY, ETHER_PRIVKEY,
                         STELLAR_PRIVKEY)
from mitumc.key.base import BaseKey
from mitumc.key.btc import to_btc_keypair
from mitumc.key.ether import to_ether_keypair
from mitumc.key.stellar import to_stellar_keypair
from rlp.sedes import List, binary, text


def _newFactSign(b, hinted_priv):
    """ Signs with provided private key and returns new FactSign object.

    Args:
        b         (bytes): Target to sign
        hinted_priv (str): Hinted private key

    Returns:
        FactSign: Generated FactSign object
    """
    assert isinstance(b, bytes), '[arg1] Must be provided in byte format'
    assert isinstance(hinted_priv, str), '[arg2] Key must be provided in string format'
    assert '-' in hinted_priv, '[arg2] Key must be hinted'

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
    """ Description for an operation.

    Attributes:
        m (text): Description
    """
    fields = (
        ('m', text),
    )
    
    @property
    def memo(self):
        return self.as_dict()['m']
    
    def to_bytes(self):
        return self.as_dict()['m'].encode()


class Amount(rlp.Serializable):
    """ Single amount.

    Attributes:
        h   (Hint): hint; MC_AMOUNT
        big  (Int): Amount in big endian integer
        cid (text): CurrencyID
    """
    fields = (
        ('h', Hint),
        ('big', Int),
        ('cid', text),
    )

    def to_bytes(self):
        # Returns concatenated [big, cid] in byte format
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
    """ Address with hint.

    Attributes:
        h    (Hint): hint; MC_ADDRESS
        addr (text): address
    """
    fields = (
        ('h', Hint),
        ('addr', text),
    )

    def hint(self):
        return self.as_dict()['h'].hint

    def hinted(self):
        # Returns hinted address
        d = self.as_dict()
        return d['addr'] + '-' + d['h'].hint

    def to_bytes(self):
        # Returns hinted address in byte format
        return self.as_dict()['addr'].encode()


class FactSign(rlp.Serializable):
    """ Single fact_sign.

    Attributes:
        h         (Hint): hint; BASE_FACT_SIGN
        signer (BaseKey): Signer's public key
        sign    (binary): Signature signed by signer
        t         (text): The time signature generated
    """
    fields = (
            ('h', Hint),
            ('signer', BaseKey),
            ('sign', binary),
            ('t', text),
        )

    def to_bytes(self):
        # Returns concatenated [signer, sign, t] in byte format
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


# skeleton: CreateAccountsFactBody, KeyUpdaterFactBody, TransfersFactBody
class OperationFactBody(rlp.Serializable):
    fields = (
        ('h', Hint),
        ('token', text),
    )

    def to_bytes(self):
        pass

    def generate_hash(self):
        pass


# skeleton: CreateAccountsFact, KeyUpdaterFact, TransfersFact
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


# skeleton: CreateAccountsBody, KeyUpdaterBody, TransfersBody
class OperationBody(rlp.Serializable):
    fields = (
        ('h', Hint),
        ('fact', OperationFact),
        ('fact_sg', List((FactSign,), False)),
    )

    def generate_hash(self):
        pass


# skeleton: CreateAccounts, KeyUpdater, Transfers
class Operation(rlp.Serializable):
    fields = (
        ('hs', Hash),
        ('body', OperationBody),
    )

    def hash(self):
        return self.as_dict()['hs']

    def to_dict(self):
        pass
