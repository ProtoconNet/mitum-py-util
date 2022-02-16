from ...common import _hint, concatBytes

class BlockCityItem(object):
    def __init__(self, type, docType, document, currencyId):
        self.hint = _hint(type)
        self.docType = docType
        self.document = document
        self.currencyId = currencyId
        
    def bytes(self):
        bDocType = self.docType.encode()
        bDocument = self.document.bytes()
        bCurrencyId = self.currencyId.encode()
        return concatBytes(bDocType, bDocument, bCurrencyId)
    
    def dict(self):
        item = {}
        
        item['_hint'] = self.hint.hint
        item['doctype'] = self.docType
        item['doc'] = self.document.dict()
        item['currency'] = self.currencyId
        
        return item