import base64

from mitumc.common import bconcat
from mitumc.hash import sha
from mitumc.operation import OperationFact, OperationFactBody


class CreateAccountsItem(object):
    """ Single CreateAccountsItem.

    Attributes:
        h               (Hint): hint; MC_CREATE_ACCOUNTS_SINGLE_AMOUNT
        ks              (Keys): Keys object for single item
        amounts (List(Amount)): List of amounts
    """
    def __init__(self, h, ks, amounts):
        self.h = h
        self.ks = ks
        self.amounts = amounts

    def to_bytes(self):
        # Returns concatenated [ks, amounts] in byte format
        amounts = self.amounts

        bamounts = bytearray()
        for amount in amounts:
            bamounts += bytearray(amount.to_bytes())

        bkeys = self.ks.to_bytes()
        bamounts = bytes(bamounts)

        return bconcat(bkeys, bamounts)

    def to_dict(self):
        item = {}
        item['_hint'] = self.h.hint
        item['keys'] = self.ks.to_dict()
        
        _amounts = self.amounts
        amounts = list()
        for _amount in _amounts:
            amounts.append(_amount.to_dict())
        item['amounts'] = amounts

        return item


class CreateAccountsFactBody(OperationFactBody):
    """ Body of CreateAccountsFact.

    Attributes:
        h                         (Hint): hint; MC_CREATE_ACCOUNTS_OP_FACT
        token                      (str): base64 encoded fact token
        sender                 (Address): Sender address
        items (List(CreateAccountsItem)): List of items
    """
    def __init__(self, h, token, sender, items):
        super(CreateAccountsFactBody, self).__init__(h, token)
        self.sender = sender
        self.items = items

    def to_bytes(self):
        # Returns concatenated [token, sender, items] in byte format

        bitems = bytearray()
        for i in self.items:
            bitems += bytearray(i.to_bytes())
        
        btoken = self.token.encode()
        bsender = self.sender.hinted().encode()
        bitems = bytes(bitems)

        return bconcat(btoken, bsender, bitems)

    def generate_hash(self):
        return sha.sum256(self.to_bytes())


class CreateAccountsFact(OperationFact):
    """ Contains CreateAccountsFactBody and a hash.

    Attributes:
        hs                     (Hash): Fact Hash
        body (CreateAccountsFactBody): Fact body object
    """
    def __init__(self, hs, body):
        super(CreateAccountsFact, self).__init__(hs, body)

    def hash(self):
        return self.hs

    def to_dict(self):
        d = self.body
        fact = {}
        fact['_hint'] = d.h.hint
        fact['hash'] = self.hash().hash
        token = base64.b64encode(d.token.encode('ascii')).decode('ascii')
        fact['token'] = token
        fact['sender'] = d.sender.hinted()

        _items = list()
        for item in d.items:
            _items.append(item.to_dict())
        fact['items'] = _items
        return fact
        