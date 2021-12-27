from mitumc.operation.generator import Generator, JSONParser

source_priv = "Kz6xZP4RQcFjD47vZ8f1hbbEomvNFUUhY7TZeu5DnXBU4ggqC4rKmpr"
source_addr = "5om5ZuSsqjEj7CxoF1VyLLJYhQoCwBPjUciy9gu8dh8hmca"
target_pub = "2BfVL17JezsZjsYx3PzXW9aRzERFA4F2Hnj1bFK7akXhAmpu"

generator = Generator('mitum')
_keys = [generator.key(target_pub, 100)]
keys = generator.createKeys(_keys, 100)

_amounts = [generator.amount(100, 'MCC')]
amounts = generator.createAmounts(_amounts)

_createAccountsItem = generator.createCreateAccountsItem(keys, amounts)
createAccountsItems = [_createAccountsItem]

createAccountsFact = generator.createCreateAccountsFact(source_addr, createAccountsItems)

createAccounts = generator.createOperation(createAccountsFact, "")
createAccounts.addFactSign(source_priv)

createAccounts.json('../example/create_accounts.json')

seal = generator.createSeal(source_priv, [createAccounts])

# print(JSONParser.toJSONString(seal))
JSONParser.generateFile(seal, '../example/seal.json')