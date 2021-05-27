import json

import base58
from mitumc.common import (Hint, bconcat, iso8601TimeStamp, parseAddress,
                           parseISOtoUTC)
from mitumc.constant import VERSION
from mitumc.hash import sha
from mitumc.hint import (BASE_FACT_SIGN, BTC_PRIVKEY, ETHER_PRIVKEY,
                         STELLAR_PRIVKEY)
from mitumc.key.btc import to_btc_keypair
from mitumc.key.ether import to_ether_keypair
from mitumc.key.stellar import to_stellar_keypair


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


class Memo(object):
    """ Description for an operation.

    Attributes:
        m (str): Description
    """
    def __init__(self, memo):
        self.memo = memo
    
    def to_bytes(self):
        return self.memo.encode()


class Amount(object):
    """ Single amount.

    Attributes:
        h   (Hint): hint; MC_AMOUNT
        big  (Int): Amount in big endian integer
        cid (str): CurrencyID
    """
    def __init__(self, h, big, cid):
        self.h = h
        self.big = big
        self.cid = cid

    def to_bytes(self):
        # Returns concatenated [big, cid] in byte format
        bbig = self.big.tight_bytes()
        bcid = self.cid.encode()

        return bconcat(bbig, bcid)

    def to_dict(self):
        amount = {}
        amount['_hint'] = self.h.hint
        amount['amount'] = str(self.big.value)
        amount['currency'] = self.cid
        return amount


class Address(object):
    """ Address with hint.

    Attributes:
        h    (Hint): hint; MC_ADDRESS
        addr (str): address
    """
    def __init__(self, h, addr):
        self.h = h
        self.addr = addr

    def hint(self):
        return self.h.hint

    def hinted(self):
        # Returns hinted address
        return self.addr + '-' + self.h.hint

    def to_bytes(self):
        # Returns hinted address in byte format
        return self.addr.encode()


class FactSign(object):
    """ Single fact_sign.

    Attributes:
        h         (Hint): hint; BASE_FACT_SIGN
        signer (BaseKey): Signer's public key
        sign    (binary): Signature signed by signer
        t         (str): The time signature generated
    """
    def __init__(self, h, signer, sign, t):
        self.h = h
        self.signer = signer
        self.sign = sign
        self.t = t

    def to_bytes(self):
        # Returns concatenated [signer, sign, t] in byte format
        bsigner = self.signer.hinted().encode()
        bsign = self.sign
        btime = parseISOtoUTC(self.t).encode()

        return bconcat(bsigner, bsign, btime)

    def signed_at(self):
       return self.t[:26] + 'Z'

    def to_dict(self):
        fact_sign = {}
        fact_sign['_hint'] = self.h.hint
        fact_sign['signer'] = self.signer.hinted()
        fact_sign['signature'] = base58.b58encode(self.sign).decode()
        fact_sign['signed_at'] = self.signed_at()
        return fact_sign


# skeleton: CreateAccountsFactBody, KeyUpdaterFactBody, TransfersFactBody
class OperationFactBody(object):
    def __init__(self, h, token):
        self.h = h
        self.token = token


# skeleton: CreateAccountsFact, KeyUpdaterFact, TransfersFact
class OperationFact(object):
    def __init__(self, hs, body):
        self.hs = hs
        self.body = body

    def hash(self):
        return self.hs

    def newFactSign(self, net_id, priv):
        # Generate a fact_sign object for provided network id and private key
        assert isinstance(net_id, str), '[arg1] Network ID must be provided as string format'

        b = bconcat(self.hash().digest, net_id.encode())
        return _newFactSign(b, priv)


class OperationBody(object):
    """ Body of Operation.

    Attributes:
        memo        (Memo): Description
        h           (Hint): hint; MC_[OPERATION-TYPE]_OP
        fact        (Fact): Fact object corresponding operation-type
        fact_sg (FactSign): List of fact signatures
    """
    def __init__(self, memo, h, fact, fact_sg):
        self.memo = memo
        self.h = h
        self.fact = fact
        self.fact_sg = fact_sg

    def to_bytes(self):
        # Returns concatenated [fact.hs, fact_sg, memo] in byte format
        bfact_hs = self.fact.hash().digest
        bmemo = self.memo.to_bytes()

        fact_sg = self.fact_sg
        bfact_sg = bytearray()
        for sg in fact_sg:
            bfact_sg += bytearray(sg.to_bytes())
        bfact_sg = bytes(bfact_sg)

        return bconcat(bfact_hs, bfact_sg, bmemo)

    def generate_hash(self):
        return sha.sum256(self.to_bytes())


class Operation(object):
    """ Operation.

    Attributes:
        hs (Hash): Operation Hash
        body (Body): Body object corresponding operation-type
    """
    def __init__(self, hs, body):
        self.hs = hs
        self.body = body

    def hash(self):
        return self.hs

    def to_dict(self):
        d = self.body
        oper = {}
        oper['memo'] = d.memo.memo
        oper['_hint'] = d.h.hint
        oper['fact'] = d.fact.to_dict()
        oper['hash'] = self.hash().hash

        fact_signs = list()
        for _sg in d.fact_sg:
            fact_signs.append(_sg.to_dict())
        oper['fact_signs'] = fact_signs

        return oper

    def to_json(self, file_name):
        with open(file_name, "w") as fp:
            json.dump(self.to_dict(), fp)
