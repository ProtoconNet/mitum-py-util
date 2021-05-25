import base64
import json

import rlp
from mitumc.common import Hash, Hint, bconcat
from mitumc.hash import sha
from mitumc.operation import (Address, Amount, FactSign, Memo, Operation,
                             OperationBody, OperationFact, OperationFactBody)
from mitumc.operation.base import _newFactSign
from rlp.sedes import List, text


class TransfersItem(rlp.Serializable):
    fields = (
        ('h', Hint),
        ('receiver', Address),
        ('amounts', List((Amount, ), False)),
    )

    def to_bytes(self):
        d = self.as_dict()
        amounts = d['amounts']

        bamounts = bytearray()
        for amount in amounts:
            bamounts += bytearray(amount.to_bytes())

        breceiver = d['receiver'].hinted().encode()
        bamounts = bytes(bamounts)
        
        return bconcat(breceiver, bamounts)

    def to_dict(self):
        d = self.as_dict()
        item = {}
        item['_hint'] = d['h'].hint
        item['receiver'] = d['receiver'].hinted()
        
        amounts = list()
        _amounts = d['amounts']
        for _amount in _amounts:
            amounts.append(_amount.to_dict())
        item['amounts'] = amounts

        return item


class TransfersFactBody(OperationFactBody):
    fields = (
        ('h', Hint),
        ('token', text),
        ('sender', Address),
        ('items', List((TransfersItem, ), False)),
    )

    def to_bytes(self):
        d = self.as_dict()
        items = d['items']

        bitems = bytearray()
        for i in items:
            bitems += bytearray(i.to_bytes())

        btoken = d['token'].encode()
        bsender = d['sender'].hinted().encode()
        bitems = bytes(bitems)

        return bconcat(btoken, bsender, bitems)

    def generate_hash(self):
        return sha.sum256(self.to_bytes())


class TransfersFact(OperationFact):
    fields = (
        ('hs', Hash),
        ('body', TransfersFactBody),
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
        fact['sender'] = d['sender'].hinted()

        items = list()
        _items = d['items']
        for _item in _items:
            items.append(_item.to_dict())
        fact['items'] = items

        return fact


class TransfersBody(OperationBody):
    fields = (
        ('memo', Memo),
        ('h', Hint),
        ('fact', TransfersFact),
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


class Transfers(Operation):
    fields = (
        ('hs', Hash),
        ('body', TransfersBody),
    )

    def hash(self):
        return self.as_dict()['hs']

    def to_dict(self):
        d = self.as_dict()['body'].as_dict()
        oper = {}
        oper['memo'] = d['memo'].memo
        oper['_hint'] = d['h'].hint
        oper['fact'] = d['fact'].to_dict()

        fact_signs = list()
        _sgs = d['fact_sg']
        for _sg in _sgs:
            fact_signs.append(_sg.to_dict())
        oper['fact_signs'] = fact_signs

        oper['hash'] = self.hash().hash

        return oper

    def to_json(self, file_name):
        with open(file_name, "w") as fp:
            json.dump(self.to_dict(), fp)
