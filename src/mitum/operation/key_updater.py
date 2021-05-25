import base64
import json

from mitum.common import Hash, Hint, bconcat
from mitum.hash import sha
from mitum.key.base import Keys
from mitum.operation import (Address, FactSign, Memo, Operation, OperationBody,
                             OperationFact, OperationFactBody)
from mitum.operation.base import _newFactSign
from rlp.sedes import List, text


class KeyUpdaterFactBody(OperationFactBody):
    fields = (
        ('h', Hint),
        ('token', text),
        ('target', Address),
        ('cid', text),
        ('ks', Keys),
    )
    
    def to_bytes(self):
        d = self.as_dict()

        btoken = d['token'].encode()
        btarget = d['target'].hinted().encode()
        bkeys = d['ks'].to_bytes()
        bcid = d['cid'].encode()
      
        return bconcat(btoken, btarget, bkeys, bcid)

    def generate_hash(self):
        return sha.sum256(self.to_bytes())
    

class KeyUpdaterFact(OperationFact):
    fields = (
        ('hs', Hash),
        ('body', KeyUpdaterFactBody),
    )

    def hash(self):
        return self.as_dict()['hs']
        
    def newFactSign(self, net_id, priv):
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


class KeyUpdaterBody(OperationBody):
    fields = (
        ('memo', Memo),
        ('h', Hint),
        ('fact', KeyUpdaterFact),
        ('fact_sg', List((FactSign,), False)),
    )

    def to_bytes(self):
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
