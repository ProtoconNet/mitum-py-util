import base64
import json

from mitumc.common import Hash, Hint, bconcat
from mitumc.hash import sha
from mitumc.key.base import Keys
from mitumc.operation import (Address, FactSign, Memo, Operation, OperationBody,
                             OperationFact, OperationFactBody)
from mitumc.operation.base import _newFactSign
from rlp.sedes import List, text


class KeyUpdaterFactBody(OperationFactBody):
    """ Body of KeyUpdaterFact.

    Attributes:
        h         (Hint): hint; MC_KEYUPDATER_OP_FACT
        tok       (text): base64 encoded fact token
        target (Address): Target Address
        cid       (text): CurrencyID
        ks        (Keys): Keys object
    """
    fields = (
        ('h', Hint),
        ('token', text),
        ('target', Address),
        ('cid', text),
        ('ks', Keys),
    )
    
    def to_bytes(self):
        # Returns concatenated [token, target, ks, cid] in byte format
        d = self.as_dict()

        btoken = d['token'].encode()
        btarget = d['target'].hinted().encode()
        bkeys = d['ks'].to_bytes()
        bcid = d['cid'].encode()
      
        return bconcat(btoken, btarget, bkeys, bcid)

    def generate_hash(self):
        return sha.sum256(self.to_bytes())
    

class KeyUpdaterFact(OperationFact):
    """ Contains KeyUpdaterFactBody and a hash.

    Attributes:
        hs                 (Hash): Fact Hash
        body (KeyUpdaterFactBody): Fact body object
    """
    fields = (
        ('hs', Hash),
        ('body', KeyUpdaterFactBody),
    )

    def hash(self):
        return self.as_dict()['hs']
        
    def newFactSign(self, net_id, priv):
        # Generate a fact_sign object for provided network id and private key
        assert isinstance(net_id, str), '[arg1] Network ID must be provided as string format'

        b = bconcat(self.hash().digest, net_id.encode())
        return _newFactSign(b, priv)

    def to_dict(self):
        d = self.as_dict()['body'].as_dict()
        fact = {}
        fact['_hint'] = d['h'].hint
        fact['hash'] = self.hash().hash
        token = d['token'].encode('ascii')
        token = base64.b64encode(token)
        token = token.decode('ascii')
        fact['token'] = token
        fact['target'] = d['target'].hinted()
        fact['keys'] = d['ks'].to_dict()
        fact['currency'] = d['cid']
        return fact

    def to_json(self, file_name):
        with open(file_name, "w") as fp:
            json.dump(self.to_dict(), fp)


class KeyUpdaterBody(OperationBody):
    """ Body of KeyUpdater.

    Attributes:
        memo              (Memo): Description
        h                 (Hint): hint; MC_KEYUPDATER_OP
        fact    (KeyUpdaterFact): Fact object
        fact_sg (List(FactSign)): List of FactSign
    """
    fields = (
        ('memo', Memo),
        ('h', Hint),
        ('fact', KeyUpdaterFact),
        ('fact_sg', List((FactSign,), False)),
    )

    def to_bytes(self):
        # Returns concatenated [fact.hs, fact_sg, memo] in byte format
        d = self.as_dict()
        bfact_hs = d['fact'].hash().digest
        bmemo = d['memo'].to_bytes()

        fact_sg = d['fact_sg']
        bfact_sg = bytearray()
        for sg in fact_sg:
            bfact_sg += bytearray(sg.to_bytes())
        bfact_sg = bytes(bfact_sg)

        return bconcat(bfact_hs, bfact_sg, bmemo)

    def generate_hash(self):
        return sha.sum256(self.to_bytes())


class KeyUpdater(Operation):
    """ KeyUpdater operation.

    Attributes:
        hs             (Hash): Hash of operation
        body (KeyUpdaterBody): Operation body
    """
    fields = (
        ('hs', Hash),
        ('body', KeyUpdaterBody),
    )

    def hash(self):
        return self.as_dict()['hs']

    def to_dict(self):
        d = self.as_dict()['body'].as_dict()
        oper = {}
        oper['memo'] = d['memo'].memo
        oper['_hint'] = d['h'].hint
        oper['fact'] = d['fact'].to_dict()
        oper['hash'] = self.hash().hash

        fact_signs = list()
        _sgs = d['fact_sg']
        for _sg in _sgs:
            fact_signs.append(_sg.to_dict())
        oper['fact_signs'] = fact_signs

        return oper

    def to_json(self, file_name):
        with open(file_name, "w") as fp:
            json.dump(self.to_dict(), fp)
