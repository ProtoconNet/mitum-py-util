import base64

from ..currency import Amount
from ..base import PurposedOperationFact
from ...hint import (
    MF_POOL_DEPOSITS_OP, MF_POOL_DEPOSITS_OP_FACT, MF_POOL_POLICY_UPDATER_OP, MF_POOL_POLICY_UPDATER_OP_FACT,
    MF_POOL_REGISTER_OP, MF_POOL_REGISTER_OP_FACT, MF_POOL_WITHDRAW_OP, MF_POOL_WITHDRAW_OP_FACT
)
from ...hash import sha3
from ...key import Address
from ...common import _hint, concatBytes


class PoolRegisterFact(PurposedOperationFact):
    def __init__(self, sender, target, initFee, incomeCid, outgoCid, cid):
        super(PoolRegisterFact, self).__init__(MF_POOL_REGISTER_OP_FACT)
        self.sender = Address(sender)
        self.target = Address(target)
        self.initFee = Amount(initFee[0], initFee[1])
        self.incomeCid = incomeCid
        self.outgoCid = outgoCid
        self.cid = cid
        self.hash = sha3(self.bytes())

    @property
    def operationHint(self):
        return _hint(MF_POOL_REGISTER_OP)

    def bytes(self):
        bToken = self.token.encode()
        bSender = self.sender.bytes()
        bTarget = self.target.bytes()
        bInitFee = self.initFee.bytes()
        bIncomeCid = self.incomeCid.encode()
        bOutgoCid = self.outgoCid.encode()
        bCid = self.cid.encode()

        return concatBytes(bToken, bSender, bTarget, bInitFee, bIncomeCid, bOutgoCid, bCid)

    def dict(self):
        fact = {}
        fact['_hint'] = self.hint.hint
        fact['hash'] = self.hash.hash
        fact['token'] = base64.b64encode(
            self.token.encode('ascii')).decode('ascii')
        fact['sender'] = self.sender.address
        fact['target'] = self.target.address
        fact['initialfee'] = self.initFee.dict()
        fact['incomingcid'] = self.incomeCid
        fact['outgoingcid'] = self.outgoCid
        fact['currency'] = self.cid
        return fact


class PoolPolicyUpdaterFact(PurposedOperationFact):
    def __init__(self, sender, target, fee, poolId, cid):
        super(PoolPolicyUpdaterFact, self).__init__(
            MF_POOL_POLICY_UPDATER_OP_FACT)
        self.sender = Address(sender)
        self.target = Address(target)
        self.fee = Amount(fee[0], fee[1])
        self.poolId = poolId
        self.cid = cid
        self.hash = sha3(self.bytes())

    @property
    def operationHint(self):
        return _hint(MF_POOL_POLICY_UPDATER_OP)

    def bytes(self):
        bToken = self.token.encode()
        bSender = self.sender.bytes()
        bTarget = self.target.bytes()
        bFee = self.fee.bytes()
        bPoolId = self.poolId.encode()
        bCid = self.cid.encode()

        return concatBytes(bToken, bSender, bTarget, bFee, bPoolId, bCid)

    def dict(self):
        fact = {}
        fact['_hint'] = self.hint.hint
        fact['hash'] = self.hash.hash
        fact['token'] = base64.b64encode(
            self.token.encode('ascii')).decode('ascii')
        fact['sender'] = self.sender.address
        fact['target'] = self.target.address
        fact['fee'] = self.fee.dict()
        fact['poolid'] = self.poolId
        fact['currency'] = self.cid
        return fact


class PoolDepositsFact(PurposedOperationFact):
    def __init__(self, sender, pool, poolId, amount):
        super(PoolDepositsFact, self).__init__(MF_POOL_DEPOSITS_OP_FACT)
        self.sender = Address(sender)
        self.pool = Address(pool)
        self.poolId = poolId
        self.amount = Amount(amount[0], amount[1])
        self.hash = sha3(self.bytes())

    @property
    def operationHint(self):
        return _hint(MF_POOL_DEPOSITS_OP)

    def bytes(self):
        bToken = self.token.encode()
        bSender = self.sender.bytes()
        bPool = self.pool.bytes()
        bPoolId = self.poolId.encode()
        bAmount = self.amount.bytes()

        return concatBytes(bToken, bSender, bPool, bPoolId, bAmount)

    def dict(self):
        fact = {}
        fact['_hint'] = self.hint.hint
        fact['hash'] = self.hash.hash
        fact['token'] = base64.b64encode(
            self.token.encode('ascii')).decode('ascii')
        fact['sender'] = self.sender.address
        fact['pool'] = self.pool.address
        fact['poolid'] = self.poolId
        fact['amount'] = self.amount.dict()
        return fact


class PoolWithdrawFact(PurposedOperationFact):
    def __init__(self, sender, pool, poolId, amounts):
        super(PoolWithdrawFact, self).__init__(MF_POOL_WITHDRAW_OP_FACT)
        self.sender = Address(sender)
        self.pool = Address(pool)
        self.poolId = poolId
        self.amounts = []
        for amt in amounts:
            self.amounts.append(Amount(amt[0], amt[1]))
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
        bPoolId = self.poolId.encode()
        bAmounts = bytes(bAmounts)

        return concatBytes(bToken, bSender, bPool, bPoolId, bAmounts)

    def dict(self):
        fact = {}
        fact['_hint'] = self.hint.hint
        fact['hash'] = self.hash.hash
        fact['token'] = base64.b64encode(
            self.token.encode('ascii')).decode('ascii')
        fact['sender'] = self.sender.address
        fact['pool'] = self.pool.address
        fact['poolid'] = self.poolId

        _amounts = list()
        for amount in self.amounts:
            _amounts.append(amount.dict())
        fact['amounts'] = _amounts

        return fact
