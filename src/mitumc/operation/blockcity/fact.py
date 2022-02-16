import base64
from ...common import concatBytes
from ...hash import sha3
from ...key.key import Address
from .. import OperationFact


class BlockCityFact(OperationFact):
    def __init__(self, _type, sender, items):
        super(BlockCityFact, self).__init__(_type)
        
        self.type = _type
        self.sender = Address(sender) 
        self.items = items
        self.hash = sha3(self.bytes())
        
    def bytes(self):
        bItems = bytearray()
        for i in self.items:
            bItems += bytearray(i.bytes())

        bToken = self.token.encode()
        bSender = self.sender.bytes()
        bItems = bytes(bItems)

        return concatBytes(bToken, bSender, bItems)
    
    def dict(self):
        fact = {}
        
        fact['_hint'] = self.hint.hint
        fact['hash'] = self.hash.hash
        fact['token'] = base64.b64encode(self.token.encode('ascii')).decode('ascii')
        fact['sender'] = self.sender.address
        
        arr = []
        for i in self.items:
            arr.append(i.dict())
        fact['items'] = arr
        
        return fact