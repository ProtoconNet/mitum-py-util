from mitumc.operation.generator import Generator, JSONParser

source_priv = "L5GTSKkRs9NPsXwYgACZdodNUJqCAWjz2BccuR4cAgxJumEZWjok~btc-priv-v0.0.1"
source_addr = "GbymDFuVmJwP4bjjyYu4L6xgBfUmdceufrMDdn4x1oz~mca-v0.0.1"
target_pub = "GBYLIBJYZP6ZIYPFGOZSXSAPMRDA6XXRKNSMOMRCKNV2YZ35DGRPEQ35~stellar-pub-v0.0.1"

ac1_prv = "SBGISVULOQA6BPEYF4OS2JGMBST7HYCBSL3TA2QRVGRNBMVWIZVE6336~stellar-priv-v0.0.1"
ac1_pub = "GBYLIBJYZP6ZIYPFGOZSXSAPMRDA6XXRKNSMOMRCKNV2YZ35DGRPEQ35~stellar-pub-v0.0.1"
# ac1_addr= "EN99uNg2LgCjYaDW8pUBohYThwsSQRWdxkF1gJhKbC7T~mca-v0.0.1"

ac2_prv = "8d15c09377e0d504f175f8ad595690b83e59e08c67d7f71f7795a489412b6f04~ether-priv-v0.0.1"
ac2_pub = "04c7a0b69c4041d2d3cf60d9318b5fdb1c29c7f63b3514aab52db6a852083dd3e1065afa8524c4ba54688ae36055377b2bb3de931054c124f01f38e7eab27e9e8f~ether-pub-v0.0.1"
# ac2_addr = "3EMR2tXh4xFfendNfHGjFSgKgPHZYsZB7w4HKqVx7Bm6~mca-v0.0.1"

ac3_prv = "SBEJGCQ4OBOOIHFWZBEHOI6FSSTDLATDFY73QIZANP2J6KMLL77CAI4D~stellar-priv-v0.0.1"
ac3_pub = "GCV6WZ5U7HXFOXWTMLUXCG4PW3KP2YYTMAPZDE3IIVWQY7Q6SYPG63TZ~stellar-pub-v0.0.1"
ac3_addr = "HJC4YAHznWLpBCzUZh7txn6vec5rhQ7EoKFfqX9UphLF~mca-v0.0.1"

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
createAccounts.to_json('../example/create_accounts.json')

_key2 = (ac2_pub, 100)
_keys2 = [_key2]
keys2 = generator.createKeys(_keys2, 100)

keyUpdaterFact = generator.createKeyUpdaterFact(source_addr, "MCC", keys2)

keyUpdater = generator.createOperation(keyUpdaterFact, "")
keyUpdater.addFactSign(source_priv)

# print(keyUpdater.to_dict())
keyUpdater.to_json('../example/key_updater.json')

_amount2 = (100, 'MCC')
_amounts2 = [_amount2]
amounts2 = generator.createAmounts(_amounts2)

_transfersItem = generator.createTransfersItem(ac3_addr, amounts2)
transfersItems = [_transfersItem]

transfersFact = generator.createTransfersFact(source_addr, transfersItems)

transfers = generator.createOperation(transfersFact, "")
transfers.addFactSign(source_priv)

# print(transfers.to_dict())
transfers.to_json('../example/transfers.json')

operations = [createAccounts, keyUpdater, transfers]
seal = generator.createSeal(source_priv, operations)

# print(JSONParser.toJSONString(seal))
JSONParser.generateFile(seal, '../example/seal.json')