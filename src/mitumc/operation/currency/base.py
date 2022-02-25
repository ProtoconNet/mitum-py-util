from ...common import MitumFactor, _hint, concatBytes, Int

from ...hint import MC_AMOUNT


class Amount(MitumFactor):
    def __init__(self, cid, big):
        self.hint = _hint(MC_AMOUNT)
        self.big = Int(big)
        self.cid = cid

    def bytes(self):
        bBig = self.big.tight()
        bCid = self.cid.encode()

        return concatBytes(bBig, bCid)

    def dict(self):
        amount = {}
        amount['_hint'] = self.hint.hint
        amount['amount'] = str(self.big.value)
        amount['currency'] = self.cid
        return amount
