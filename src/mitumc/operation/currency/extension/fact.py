from ...base import GeneralOperationFact
from ....common import _hint
from ....hint import (
    MC_EXT_CREATE_CONTRACT_ACCOUNTS_OP, MC_EXT_CREATE_CONTRACT_ACCOUNTS_OP_FACT, 
    MC_EXT_WITHDRAWS_OP, MC_EXT_WITHDRAWS_OP_FACT
)


class CreateContractAccountsFact(GeneralOperationFact):
    def __init__(self, sender, items):
        super(CreateContractAccountsFact, self).__init__(
            MC_EXT_CREATE_CONTRACT_ACCOUNTS_OP_FACT, sender, items)

    @property
    def operationHint(self):
        return _hint(MC_EXT_CREATE_CONTRACT_ACCOUNTS_OP)


class WithdrawsFact(GeneralOperationFact):
    def __init__(self, sender, items):
        super(WithdrawsFact, self).__init__(
            MC_EXT_WITHDRAWS_OP_FACT, sender, items)

    @property
    def operationHint(self):
        return _hint(MC_EXT_WITHDRAWS_OP)
