# mitum-py-util

'mitum-py-util' will introduce the usage of mitum-currency for python.

## Installation

Recommended requirements for 'mitum-py-util' are,

* python v3.9 or later.
* base58 v2.1.0
* pybase64 v1.1.4
* ecdsa v0.13.3
* bitcoinaddress v0.1.5
* bitcoin-utils v0.4.11
* eth_keys v0.3.3
* stellar_sdk v3.3.2
* pytz v2021.1
* datetime v4.3

```sh
$ python --version
Python 3.9.2

$ git clone https://github.com/ProtoconNet/mitum-py-util.git

$ cd mitum-py-util

$ python setup.py install
```

## Generate New Operation

### Operations

'mitum-py-util' provides three operations to be generated,

* 'Create-Accounts' creates an account corresponding to any public key with a pre-registered account.
* 'Key-Updater' updates the public key of the account to something else.
* 'Transfers' transfers tokens from the account to another account.

'mitum-currency' supports various kinds of operations, but 'mitum-py-util' will provide these frequently used operations.

### Prerequisite

Before generating new operation, you should check below,

* 'private key' of source account to generate signatures (a.k.a signing key)
* 'public address' of source account
* 'public key' of target account
* 'network id'

Notice that the package name of 'mitum-py-util' is 'mitumc' for python codes.

* Every key, address, and keypair must be that of mitum-currency.

### Generator

'mitumc' package provides 'Generator' class to generate operations.

Modules that 'Generator' supports are,

```python
>>> Generator.set_id(net_id) 
>>> Generator.createKeys(keys, threshold)
>>> Generator.createAmounts(amounts) 
>>> Generator.createCreateAccountsItem(keys_o, amounts)
>>> Generator.createTransfersItem(receiver, amoutns)
>>> Generator.createCreateAccountsFact(sender, items)
>>> Generator.createKeyUpdaterFact(target, cid, keys_o)
>>> Generator.createTransfersFact(sender, items)
>>> Generator.createOperation(fact, memo)
```

You can check use-cases of Generator in the next part.

### Generate Create-Accounts 

To generate an operation, 'currency id' and 'initial amount' must be set. With source account, you can create and register new account of target public key.

When you use 'Generator', you must set 'network id' before you create something.

#### Usage

```python
>>> from mitumc.operation import Generator

>>> source_priv = "L5GTSKkRs9NPsXwYgACZdodNUJqCAWjz2BccuR4cAgxJumEZWjok:btc-priv-v0.0.1"
>>> source_addr = "GbymDFuVmJwP4bjjyYu4L6xgBfUmdceufrMDdn4x1oz:mca-v0.0.1"
>>> target_pub = "GBYLIBJYZP6ZIYPFGOZSXSAPMRDA6XXRKNSMOMRCKNV2YZ35DGRPEQ35:stellar-pub-v0.0.1"

>>> generator = Generator("mitum")

>>> key = (target_pub, 100)
>>> keys_o = generator.createKeys([_key], 100)

>>> amount = (100, "MCC")
>>> amounts = generator.createAmounts([_amount])

>>> createAccountsItem = generator.createCreateAccountsItem(keys_o, amounts)
>>> createAccountsFact = generator.createCreateAccountsFaact(source_addr, [createAccountsItem])

>>> createAccounts = generator.createOperation(createAccountsFact, "")
>>> createAccounts.addFactSign(source_priv)
```

You must add new fact signature by addFactSign before create seal or json files from an operation.

Then Operation.to_dict() and Operation.to_json(file_name) methods work correctly.

```python
>>> createAccounts.to_dict()
>>> createAccounts.to_json("create_account.json")
```

Then the result format will be like [this](example/create_accounts.json). (Each value is up to input arguments and time)


### Generate Key-Updater

Key-Updater literally supports to update cource public key to something else.

#### Usage

```python
>>> from mitumc.operation import Generator

>>> source_priv = "L5GTSKkRs9NPsXwYgACZdodNUJqCAWjz2BccuR4cAgxJumEZWjok:btc-priv-v0.0.1"
>>> source_addr = "GbymDFuVmJwP4bjjyYu4L6xgBfUmdceufrMDdn4x1oz:mca-v0.0.1"
>>> target_pub = "04c7a0b69c4041d2d3cf60d9318b5fdb1c29c7f63b3514aab52db6a852083dd3e1065afa8524c4ba54688ae36055377b2bb3de931054c124f01f38e7eab27e9e8f:ether-pub-v0.0.1"

>>> generator = Generator('mitum')

>>> key = (target_pub, 100)
>>> keys = generator.createKeys([key], 100)

>>> keyUpdaterFact = generator.createKeyUpdaterFact(source_addr, "MCC", keys)

>>> keyUpdater = generator.createOperation(keyUpdaterFact, "")
>>> keyUpdater.addFactSign(source_priv)

>>> keyUpdater.to_dict()
>>> keyUpdater.to_json("key_updater.json")
```

### Generate Transfers

To generate an operation, you must prepare target address, not public key. Transfers supports to send tokens to another account.

#### Usage

```python
>>> from mitumc.operation import Generator

>>> source_priv = "L5GTSKkRs9NPsXwYgACZdodNUJqCAWjz2BccuR4cAgxJumEZWjok:btc-priv-v0.0.1"
>>> source_addr = "GbymDFuVmJwP4bjjyYu4L6xgBfUmdceufrMDdn4x1oz:mca-v0.0.1"
>>> target_addr = "CzCW7V9Doi71dLJVXcdnS6V4BJDzvPdY28YCn1ksiG4m:mca-v0.0.1"

>>> generator = Generator('mitum')

>>> amount = (100, "MCC")
>>> amounts = generator.createAmounts([amount])

>>> transfersItem = generator.createTransfersItem(target_addr, amounts)

>>> transfersFact = generator.createTransfersFact(source_addr, [transfersItem])

>>> transfers = generator.createOperation(transfersFact, "")
>>> transfers.addFactSign(source_priv)

>>> transfers.to_dict()
>>> transfers.to_json('transfers.json')
```

## Generate New Seal

Supports you to generate a seal json file such that the seal is able to consist of several operations. Those operations can be any type 'mitum-py-util' provides.

### Prerequisite

To generate a seal, 'mitum-py-util' requires,

* 'signing key'
* 'a list of pre-constructed operations' not empty

Registration of 'signing key' is not neccessary.

### JSONParser

You can create a json file from generated seal object without 'JSONParser' class provided by 'mitumc'. However, I recommend that use 'JSONParser' for convenience.

Modules that 'JSONParser' supports are,

```python
>>> JSONParser.toJSONString(seal)
>>> JSONParser.generateFile(seal, fName)
```

A use-case of 'JSONParser' will be introduced in the next part.

### Usage

First of all, suppose that every operation is that generated by 'Generator'. (createAccounts, keyUpdater, Transfers)

### Example

```python
>>> from mitumc.operation import Generator, JSONParser

>>> generator = Generator('mitum')

... omitted
''' Create each operation [createAccounts, keyUpdater, transfers] with generator. See above sections.
'''
...

>>> source_priv = "L5GTSKkRs9NPsXwYgACZdodNUJqCAWjz2BccuR4cAgxJumEZWjok:btc-priv-v0.0.1"

>>> operations = [createAccounts, keyUpdater, transfers]
>>> seal = generator.createSeal(source_priv, operations)

>>> JSONParser.toJSONString(seal)
>>> JSONParser.generateFile(seal, 'seal.json')
```

Then the result format of generateFile() will be like [this](example/seal.json). (Each value is up to input arguments and time)

## Send Seal to Network

Created seal json files will be used to send seals by 'mitum-currency'.

Use below command to send them to the target network. (See [mitum-currency](https://github.com/ProtoconNet/mitum-currency) for details)

```sh
$ bin/mc seal send --network-id=$NETWORK_ID $SIGNING_KEY --seal=seal.json
```

* seal.json is your seal file.

## Hash Functions

'mitumc.hash' module supports sha2(sha256) and sha3(sum256) hashing.

#### Example

mitumc_hash.py
```python
>>> from mitumc.hash import sha256, sum256

>>> msg = b'mitum'
>>> sha2_hash = sha256(msg)
>>> sha3_hash = sum256(msg)

>>> print(sha2_hash.digest)
>>> print(sha2_hash.hash)
>>> print(sha3_hash.digest)
>>> print(sha3_hash.hash)
```

The result will be,

```sh
$ python mitumc_hash.py
b'\xf7.\xd28\xfd\xc1+\xfc\x1d\xa9\xcdb9y\x8cF+RW4\x89)\x99\xcb\xdc\xf5\xbe\xf5\xa7J\xf2\x95'
Hdu7PqjA1p55GAcBiULmCAfzoksdwW1oSxaMH83kw9BJ
b'jf\x10J>\xb9O]\x14\xab}d,r\x88(B\xab\x9a\xb1x\x18\x04\xeb\x10!\x9f\xebY\xa5v"'
8ALUvxZ5Q1qQEsPUcHsoAzuzEp8Bm4HQpYqNNSafjDAR
```