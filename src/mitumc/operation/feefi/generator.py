from .fact import PoolDepositsFact, PoolPolicyUpdaterFact, PoolRegisterFact, PoolWithdrawFact
from ..base import OperationGenerator


class FeefiGenerator(OperationGenerator):
    def __init__(self, id):
        super(FeefiGenerator, self).__init__(id)

    def getPoolRegisterFact(self, sender, target, initFee, incomeCid, outgoCid, cid):
        return PoolRegisterFact(sender, target, initFee, incomeCid, outgoCid, cid)
    
    def getPoolPolicyUpdaterFact(self, sender, target, fee, poolId, cid):
        return PoolPolicyUpdaterFact(sender, target, fee, poolId, cid)
    
    def getPoolDepositsFact(self, sender, pool, poolId, amount):
        return PoolDepositsFact(sender, pool, poolId, amount)
    
    def getPoolWithdrawFact(self, sender, pool, poolId, amounts):
        return PoolWithdrawFact(sender, pool, poolId, amounts)