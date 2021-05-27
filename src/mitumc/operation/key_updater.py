import base64

from mitumc.common import bconcat
from mitumc.hash import sha
from mitumc.operation import OperationFact, OperationFactBody


class KeyUpdaterFactBody(OperationFactBody):
    """ Body of KeyUpdaterFact.

    Attributes:
        h         (Hint): hint; MC_KEYUPDATER_OP_FACT
        token     (text): base64 encoded fact token
        target (Address): Target Address
        cid       (text): CurrencyID
        ks        (Keys): Keys object
    """
    def __init__(self, h, token, target, cid, ks):
        super(KeyUpdaterFactBody, self).__init__(h, token)
        self.target = target
        self.cid = cid
        self.ks = ks
    
    def to_bytes(self):
        # Returns concatenated [token, target, ks, cid] in byte format

        btoken = self.token.encode()
        btarget = self.target.hinted().encode()
        bkeys = self.ks.to_bytes()
        bcid = self.cid.encode()
      
        return bconcat(btoken, btarget, bkeys, bcid)

    def generate_hash(self):
        return sha.sum256(self.to_bytes())
    

class KeyUpdaterFact(OperationFact):
    """ Contains KeyUpdaterFactBody and a hash.

    Attributes:
        hs                 (Hash): Fact Hash
        body (KeyUpdaterFactBody): Fact body object
    """
    def __init__(self, hs, body):
        super(KeyUpdaterFact, self).__init__(hs, body)

    def to_dict(self):
        d = self.body
        fact = {}
        fact['_hint'] = d.h.hint
        fact['hash'] = self.hash().hash
        fact['token'] = base64.b64encode(d.token.encode('ascii')).decode('ascii')
        fact['target'] = d.target.hinted()
        fact['keys'] = d.ks.to_dict()
        fact['currency'] = d.cid
        return fact


