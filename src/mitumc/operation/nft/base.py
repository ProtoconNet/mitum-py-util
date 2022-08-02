from ...key import Address
from ...common import Int, concatBytes, _hint
from ...hint import MNFT_COLLECTION_POLICY, MNFT_COLLECTION_REGISTER_FORM, MNFT_MINT_FORM, MNFT_NFT_ID, MNFT_SIGNER, MNFT_SIGNERS


class CollectionRegisterForm:
    def __init__(self, target, symbol, name, royalty, uri, whites):
        assert royalty >= 0 and royalty < 100, 'Invalid royalty; CollectionRegisterForm'
        self.hint = _hint(MNFT_COLLECTION_REGISTER_FORM)
        self.target = Address(target)
        self.symbol = symbol
        self.name = name
        self.royalty = Int(royalty)
        self.uri = uri
        self.whites = []
        for w in whites:
            self.whites.append(Address(w))

    def bytes(self):
        bTarget = self.target.bytes()
        bSymbol = self.symbol.encode()
        bName = self.name.encode()
        bRoyalty = self.royalty.bytes()
        bUri = self.uri.encode()

        _whites = bytearray()
        for w in self.whites:
            _whites += w.bytes()
        bWhites = bytes(_whites)

        return concatBytes(bTarget, bSymbol, bName, bRoyalty, bUri, bWhites)

    def dict(self):
        form = {}
        form['_hint'] = self.hint.hint
        form['target'] = self.target.address
        form['symbol'] = self.symbol
        form['name'] = self.name
        form['royalty'] = self.royalty.value
        form['uri'] = self.uri

        whites = []
        for w in self.whites:
            whites.append(w.address)
        form['whites'] = whites

        return form


class CollectionPolicy:
    def __init__(self, name, royalty, uri, whites):
        assert royalty >= 0 and royalty < 100, 'Invalid royalty; CollectionPolicy'
        self.hint = _hint(MNFT_COLLECTION_POLICY)
        self.name = name
        self.royalty = Int(royalty)
        self.uri = uri
        self.whites = []
        for w in whites:
            self.whites.append(Address(w))

    def bytes(self):
        bName = self.name.encode()
        bRoyalty = self.royalty.bytes()
        bUri = self.uri.encode()
        
        _whites = bytearray()
        for w in self.whites:
            _whites += w.bytes()
        bWhites = bytes(_whites)

        return concatBytes(bName, bRoyalty, bUri, bWhites)

    def dict(self):
        policy = {}
        policy['_hint'] = self.hint.hint
        policy['name'] = self.name
        policy['royalty'] = self.royalty.value
        policy['uri'] = self.uri
        
        whites = []
        for w in self.whites:
            whites.append(w.address)
        policy['whites'] = whites

        return policy


class NFTSigner:
    def __init__(self, account, share, signed):
        assert share >= 0 and share <= 100, 'Invalid share; NFTSigner'
        self.hint = _hint(MNFT_SIGNER)
        self.account = Address(account)
        self.share = Int(share)
        self.signed = signed

    def bytes(self):
        bAccount = self.account.bytes()
        bShare = self.share.bytes()
        bSigned = bytes([0])
        if self.signed:
            bSigned = bytes([1])
        return concatBytes(bAccount, bShare, bSigned)

    def dict(self):
        signer = {}
        signer['_hint'] = self.hint.hint
        signer['account'] = self.account.address
        signer['share'] = self.share.value
        signer['signed'] = self.signed
        return signer


class NFTSigners:
    def __init__(self, total, signers):
        assert total >= 0 and total <= 100, 'Invalid total share; NFTSigners'
        self.hint = _hint(MNFT_SIGNERS)
        self.total = Int(total)
        self.signers = signers

    def bytes(self):
        bTotal = self.total.bytes()
        _signers = bytearray()
        for s in self.signers:
            _signers += s.bytes()
        bSigners = _signers

        return concatBytes(bTotal, bSigners)

    def dict(self):
        signers = {}
        signers['_hint'] = self.hint.hint
        signers['total'] = self.total.value
        _signers = []
        for s in self.signers:
            _signers.append(s.dict())
        signers['signers'] = _signers

        return signers


class MintForm:
    def __init__(self, hash, uri, creators, copyrighters):
        self.hint = _hint(MNFT_MINT_FORM)
        self.hash = hash
        self.uri = uri
        self.creators = creators
        self.copyrighters = copyrighters

    def bytes(self):
        bHash = self.hash.encode()
        bUri = self.uri.encode()
        bCreators = self.creators.bytes()
        bCopyrighters = self.copyrighters.bytes()

        return concatBytes(bHash, bUri, bCreators, bCopyrighters)

    def dict(self):
        form = {}
        form['_hint'] = self.hint.hint
        form['hash'] = self.hash
        form['uri'] = self.uri
        form['creators'] = self.creators.dict()
        form['copyrighters'] = self.copyrighters.dict()
        return form


class NFTID:
    def __init__(self, collection, idx):
        assert idx.value > 0, 'idx must be over zero; NFTID'
        self.hint = _hint(MNFT_NFT_ID)
        self.collection = collection
        self.idx = idx

    def bytes(self):
        bCollection = self.collection.encode()
        bIdx = self.idx.bytes()
        return concatBytes(bCollection, bIdx)

    def dict(self):
        id = {}
        id['_hint'] = self.hint.hint
        id['collection'] = self.collection
        id['idx'] = self.idx.value
        return id
