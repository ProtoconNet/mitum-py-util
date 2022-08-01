from .fact import CreateContractAccountsFact, WithdrawsFact
from .item import CreateContractAccountsItem, WithdrawsItem
from ...base import OperationGenerator
from ....hint import MC_EXT_CREATE_CONTRACT_ACCOUNTS_MULTIPLE_AMOUNTS, MC_EXT_WITHDRAWS_MULTIPLE_AMOUNTS


class CurrencyExtensionGenerator(OperationGenerator):
    def __init__(self, id):
        super(CurrencyExtensionGenerator, self).__init__(id)

    def getCreateContractAccountsItem(self, keys, amounts):
        # if len(amounts) > 1:
        #     return CreateContractAccountsItem(MC_EXT_CREATE_CONTRACT_ACCOUNTS_MULTIPLE_AMOUNTS, keys, amounts)
        # else:
        #     return CreateContractAccountsItem(MC_EXT_CREATE_CONTRACT_ACCOUNTS_SINGLE_AMOUNT, keys, amounts)
        return CreateContractAccountsItem(MC_EXT_CREATE_CONTRACT_ACCOUNTS_MULTIPLE_AMOUNTS, keys, amounts)

    def getWithdrawsItem(self, target, amounts):
        # if len(amounts) > 1:
        #     return WithdrawsItem(MC_EXT_WITHDRAWS_MULTIPLE_AMOUNTS, target, amounts)
        # else:
        #     return WithdrawsItem(MC_EXT_WITHDRAWS_SINGLE_AMOUNT, target, amounts)
        return WithdrawsItem(MC_EXT_WITHDRAWS_MULTIPLE_AMOUNTS, target, amounts)

    def getCreateContractAccountsFact(self, sender, items):
        return CreateContractAccountsFact(sender, items)

    def getWithdrawsFact(self, sender, items):
        return WithdrawsFact(sender, items)
