from mitumc.operation.generator import Generator, JSONParser

source_priv = "L1V19fBjhnxNyfuXLWw6Y5mjFSixzdsZP4obkXEERskGQNwSgdm1mpr"
source_addr = "5fbQg8K856KfvzPiGhzmBMb6WaL5AsugUnfutgmWECPbmca"
target_pub = "2177RF13ZZXpdE1wf7wu5f9CHKaA2zSyLW5dk18ExyJ84mpu"

ac1_prv = "KwsWqjb6stDe5x6cdN6Xz4aNiina5HK8SmWXSCc1LMXE252gTD39mpr"
ac1_pub = "buSmGvywmR6TgRXaH2gy3WWvHPTiWDYZsJu1VMnY3gaYmpu"
# ac1_addr= "EN99uNg2LgCjYaDW8pUBohYThwsSQRWdxkF1gJhKbC7T~mca-v0.0.1"

ac2_prv = "KzeNgknfsYfgxwZVqRoUx275ansnokLiYgMCjEgLVUpU2axetU6umpr"
ac2_pub = "2BqW3iy3bb9Z1fS21opL3z4da69K25d9zR5DM2CnSuNYxmpu"
# ac2_addr = "3EMR2tXh4xFfendNfHGjFSgKgPHZYsZB7w4HKqVx7Bm6~mca-v0.0.1"

ac3_prv = "L2AJFiNcyC6gzbTQMpD7QRD6UUGnAFzDfcCFv68MPNqoYP4NGM9Cmpr"
ac3_pub = "tjX9kWwUJaosuGvmiLQZy5aipq2fzDZLXfn21a5iK91impu"
ac3_addr = "D2KjoTG6yhE64jGQu7y2hUYPzRoJ2RDcnPsWrtLBDaPTmca"

generator = Generator('mitum')

_key = (ac1_pub, 100)
_keys = [_key]
keys = generator.createKeys(_keys, 100)

_amount = (100, 'MCC')
_amounts = [_amount]
amounts = generator.createAmounts(_amounts)

_createAccountsItem = generator.createCreateAccountsItem(keys, amounts)
createAccountsItems = [_createAccountsItem]

createAccountsFact = generator.createCreateAccountsFact(source_addr, createAccountsItems)

createAccounts = generator.createOperation(createAccountsFact, "")
createAccounts.addFactSign(source_priv)

# print(createAccounts.to_dict())
createAccounts.json('../example/create_accounts.json')

_key2 = (ac2_pub, 100)
_keys2 = [_key2]
keys2 = generator.createKeys(_keys2, 100)

keyUpdaterFact = generator.createKeyUpdaterFact(source_addr, keys2, "MCC")

keyUpdater = generator.createOperation(keyUpdaterFact, "")
keyUpdater.addFactSign(source_priv)

# print(keyUpdater.to_dict())
keyUpdater.json('../example/key_updater.json')

_amount2 = (100, 'MCC')
_amounts2 = [_amount2]
amounts2 = generator.createAmounts(_amounts2)

_transfersItem = generator.createTransfersItem(ac3_addr, amounts2)
transfersItems = [_transfersItem]

transfersFact = generator.createTransfersFact(source_addr, transfersItems)

transfers = generator.createOperation(transfersFact, "")
transfers.addFactSign(source_priv)

# print(transfers.to_dict())
transfers.json('../example/transfers.json')

operations = [createAccounts, keyUpdater, transfers]
seal = generator.createSeal(source_priv, operations)

# print(JSONParser.toJSONString(seal))
JSONParser.generateFile(seal, '../example/seal.json')