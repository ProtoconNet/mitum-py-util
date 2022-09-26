from .fact import PoolDepositsFact, PoolPolicyUpdaterFact, PoolRegisterFact, PoolWithdrawFact
from ..base import OperationGenerator


class FeefiGenerator(OperationGenerator):
    def __init__(self, id):
        super(FeefiGenerator, self).__init__(id)

    def getPoolRegisterFact(self, sender, target, initFee, incomeCid, outlayCid, cid):
        return PoolRegisterFact(sender, target, initFee, incomeCid, outlayCid, cid)

    def getPoolPolicyUpdaterFact(self, sender, target, fee, incomeCid, outlayCid, cid):
        return PoolPolicyUpdaterFact(sender, target, fee, incomeCid, outlayCid, cid)

    def getPoolDepositsFact(self, sender, pool, incomeCid, outlayCid, amount):
        return PoolDepositsFact(sender, pool, incomeCid, outlayCid, amount)

    def getPoolWithdrawFact(self, sender, pool, incomeCid, outlayCid, amounts):
        return PoolWithdrawFact(sender, pool, incomeCid, outlayCid, amounts)
