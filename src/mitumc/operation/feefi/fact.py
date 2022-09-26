import base64

from ..currency import Amount
from ..base import PurposedOperationFact
from ...hint import (
    MF_POOL_DEPOSITS_OP, MF_POOL_DEPOSITS_OP_FACT, MF_POOL_POLICY_UPDATER_OP, MF_POOL_POLICY_UPDATER_OP_FACT,
    MF_POOL_REGISTER_OP, MF_POOL_REGISTER_OP_FACT, MF_POOL_WITHDRAW_OP, MF_POOL_WITHDRAW_OP_FACT
)
from ...hash import sha3
from ...key import Address
from ...common import Int, _hint, concatBytes


class PoolRegisterFact(PurposedOperationFact):
    def __init__(self, sender, target, initFee, incomeCid, outlayCid, cid):
        super(PoolRegisterFact, self).__init__(MF_POOL_REGISTER_OP_FACT)
        self.sender = Address(sender)
        self.target = Address(target)
        self.initFee = Int(initFee)
        self.incomeCid = incomeCid
        self.outlayCid = outlayCid
        self.cid = cid
        self.hash = sha3(self.bytes())

    @property
    def operationHint(self):
        return _hint(MF_POOL_REGISTER_OP)

    def bytes(self):
        bToken = self.token.encode()
        bSender = self.sender.bytes()
        bTarget = self.target.bytes()
        bInitFee = self.initFee.tight()
        bIncomeCid = self.incomeCid.encode()
        bOutlayCid = self.outlayCid.encode()
        bCid = self.cid.encode()

        return concatBytes(bToken, bSender, bTarget, bInitFee, bIncomeCid, bOutlayCid, bCid)

    def dict(self):
        fact = {}
        fact['_hint'] = self.hint.hint
        fact['hash'] = self.hash.hash
        fact['token'] = base64.b64encode(
            self.token.encode('ascii')).decode('ascii')
        fact['sender'] = self.sender.address
        fact['target'] = self.target.address
        fact['initialfee'] = str(self.initFee.value)
        fact['incomecid'] = self.incomeCid
        fact['outlaycid'] = self.outlayCid
        fact['currency'] = self.cid
        return fact


class PoolPolicyUpdaterFact(PurposedOperationFact):
    def __init__(self, sender, target, fee, incomeCid, outlayCid, cid):
        super(PoolPolicyUpdaterFact, self).__init__(
            MF_POOL_POLICY_UPDATER_OP_FACT)
        self.sender = Address(sender)
        self.target = Address(target)
        self.fee = Int(fee)
        self.incomeCid = incomeCid
        self.outlayCid = outlayCid
        self.cid = cid
        self.hash = sha3(self.bytes())

    @property
    def operationHint(self):
        return _hint(MF_POOL_POLICY_UPDATER_OP)

    def bytes(self):
        bToken = self.token.encode()
        bSender = self.sender.bytes()
        bTarget = self.target.bytes()
        bFee = self.fee.tight()
        bIncomeCid = self.incomeCid.encode()
        bOutlayCid = self.outlayCid.encode()
        bCid = self.cid.encode()

        return concatBytes(bToken, bSender, bTarget, bFee, bIncomeCid, bOutlayCid, bCid)

    def dict(self):
        fact = {}
        fact['_hint'] = self.hint.hint
        fact['hash'] = self.hash.hash
        fact['token'] = base64.b64encode(
            self.token.encode('ascii')).decode('ascii')
        fact['sender'] = self.sender.address
        fact['target'] = self.target.address
        fact['fee'] = str(self.fee.value)
        fact['incomecid'] = self.incomeCid
        fact['outlaycid'] = self.outlayCid
        fact['currency'] = self.cid
        return fact


class PoolDepositsFact(PurposedOperationFact):
    def __init__(self, sender, pool, incomeCid, outlayCid, amount):
        super(PoolDepositsFact, self).__init__(MF_POOL_DEPOSITS_OP_FACT)
        self.sender = Address(sender)
        self.pool = Address(pool)
        self.incomeCid = incomeCid
        self.outlayCid = outlayCid
        self.amount = Int(amount)
        self.hash = sha3(self.bytes())

    @property
    def operationHint(self):
        return _hint(MF_POOL_DEPOSITS_OP)

    def bytes(self):
        bToken = self.token.encode()
        bSender = self.sender.bytes()
        bPool = self.pool.bytes()
        bIncomeCid = self.incomeCid.encode()
        bOutlayCid = self.outlayCid.encode()
        bAmount = self.amount.tight()

        return concatBytes(bToken, bSender, bPool, bIncomeCid, bOutlayCid, bAmount)

    def dict(self):
        fact = {}
        fact['_hint'] = self.hint.hint
        fact['hash'] = self.hash.hash
        fact['token'] = base64.b64encode(
            self.token.encode('ascii')).decode('ascii')
        fact['sender'] = self.sender.address
        fact['pool'] = self.pool.address
        fact['amount'] = str(self.amount.value)
        fact['incomecid'] = self.incomeCid
        fact['outlaycid'] = self.outlayCid
        return fact


class PoolWithdrawFact(PurposedOperationFact):
    def __init__(self, sender, pool, incomeCid, outlayCid, amounts):
        super(PoolWithdrawFact, self).__init__(MF_POOL_WITHDRAW_OP_FACT)
        self.sender = Address(sender)
        self.pool = Address(pool)
        self.incomeCid = incomeCid
        self.outlayCid = outlayCid
        self.amounts = amounts
        self.hash = sha3(self.bytes())

    @property
    def operationHint(self):
        return _hint(MF_POOL_WITHDRAW_OP)

    def bytes(self):
        bAmounts = bytearray()
        for amt in self.amounts:
            bAmounts += bytearray(amt.bytes())

        bToken = self.token.encode()
        bSender = self.sender.bytes()
        bPool = self.pool.bytes()
        bIncomeCid = self.incomeCid.encode()
        bOutlayCid = self.outlayCid.encode()
        bAmounts = bytes(bAmounts)

        return concatBytes(bToken, bSender, bPool, bIncomeCid, bOutlayCid, bAmounts)

    def dict(self):
        fact = {}
        fact['_hint'] = self.hint.hint
        fact['hash'] = self.hash.hash
        fact['token'] = base64.b64encode(
            self.token.encode('ascii')).decode('ascii')
        fact['sender'] = self.sender.address
        fact['pool'] = self.pool.address
        fact['incomecid'] = self.incomeCid
        fact['outlaycid'] = self.outlayCid

        _amounts = list()
        for amount in self.amounts:
            _amounts.append(amount.dict())
        fact['amounts'] = _amounts

        return fact
