from mitumc import Generator, JSONParser

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
gn = generator.mc

_key = gn.key(ac1_pub, 100)
_keys = [_key]
keys = gn.keys(_keys, 100)

_amount = gn.amount('MCC', 100)
_amounts = [_amount]
amounts = gn.amounts(_amounts)

_createAccountsItem = gn.getCreateAccountsItem(keys, amounts)
createAccountsItems = [_createAccountsItem]

createAccountsFact = gn.getCreateAccountsFact(source_addr, createAccountsItems)

createAccounts = generator.getOperation(createAccountsFact, "")
createAccounts.addFactSign(source_priv)

# print(createAccounts.to_dict())
createAccounts.json('example/create_accounts.json')

_key2 = gn.key(ac2_pub, 100)
_keys2 = [_key2]
keys2 = gn.keys(_keys2, 100)

keyUpdaterFact = gn.getKeyUpdaterFact(source_addr, keys2, "MCC")

keyUpdater = generator.getOperation(keyUpdaterFact, "")
keyUpdater.addFactSign(source_priv)

# print(keyUpdater.to_dict())
keyUpdater.json('example/key_updater.json')

_amount2 = gn.amount('MCC', 100)
_amounts2 = [_amount2]
amounts2 = gn.amounts(_amounts2)

_transfersItem = gn.getTransfersItem(ac3_addr, amounts2)
transfersItems = [_transfersItem]

transfersFact = gn.getTransfersFact(source_addr, transfersItems)

transfers = generator.getOperation(transfersFact, "")
transfers.addFactSign(source_priv)

# print(transfers.to_dict())
transfers.json('example/transfers.json')

operations = [createAccounts, keyUpdater, transfers]
seal = generator.getSeal(source_priv, operations)

# print(JSONParser.toJSONString(seal))
JSONParser.toFile(seal, 'example/seal.json')