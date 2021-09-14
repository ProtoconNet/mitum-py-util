# mitum-py-util

'mitum-py-util' will introduce the usage of [mitum-currency](https://github.com/ProtoconNet/mitum-currency) and [mitum-data-blocksign](https://github.com/ProtoconNet/mitum-data-blocksign) for python.

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

If setup.py doesn't work properly, please just install necessary packages with requirements.txt before running setup.py.

```sh
$ cd mitum-py-util

$ pip install -r requirements.txt
```

## Generate New Operation

### Operations

'mitum-py-util' provides three operations of 'mitum-currency',

* 'Create-Accounts' creates an account corresponding to any public key with a pre-registered account.
* 'Key-Updater' updates the public key of the account to something else.
* 'Transfers' transfers tokens from the account to another account.

'mitum-currency' supports various kinds of operations, but 'mitum-py-util' will provide these frequently used operations.

In addition, 'mitum-py-util' provides three operations of 'mitum-data-blocksign',

* 'Create-Documents' creates an document with filehash.
* 'Sign-Documents' signs the document.
* 'Transfer-Documents' transfers documents from the account to another account.

### Prerequisite

Before generating new operation, you should check below for 'mitum-currency',

* 'private key' of source account to generate signatures (a.k.a signing key)
* 'public address' of source account
* 'public key' of target account
* 'network id'

Additionally, you should check below for 'mitum-data-blocksign',

* 'filehash' for Create-Documents
* 'owner' and 'documentid' for Sign-Documents and Transfer-Documents

Note that the package name of 'mitum-py-util' is 'mitumc' for python codes.

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
>>> Generator.createCreateDocumentsItem(filehash, did, signcode, title, size, cid, signers, signcodes)
>>> Generator.createSignDocumentsItem(owner, documentid, cid)
>>> Generator.createTransferDocumentsItem(owner, receiver, documentid, cid)
>>> Generator.createCreateAccountsFact(sender, items)
>>> Generator.createKeyUpdaterFact(target, cid, keys_o)
>>> Generator.createTransfersFact(sender, items)
>>> Generator.createOperation(fact, memo)
```

You can check use-cases of Generator in the next part.

### Generate Create-Accounts 

For new account, 'currency id' and 'initial amount' must be set. With source account, you can create and register new account of target public key.

When you use 'Generator', you must set 'network id' before you create something.

#### Usage

```python
>>> from mitumc.operation import Generator

>>> source_priv = "L5GTSKkRs9NPsXwYgACZdodNUJqCAWjz2BccuR4cAgxJumEZWjok:btc-priv-v0.0.1"
>>> source_addr = "GbymDFuVmJwP4bjjyYu4L6xgBfUmdceufrMDdn4x1oz:mca-v0.0.1"
>>> target_pub = "GBYLIBJYZP6ZIYPFGOZSXSAPMRDA6XXRKNSMOMRCKNV2YZ35DGRPEQ35:stellar-pub-v0.0.1"

>>> generator = Generator("mitum")

>>> key = (target_pub, 100)
>>> keys_o = generator.createKeys([key], 100)

>>> amount = (100, "MCC")
>>> amounts = generator.createAmounts([amount])

>>> createAccountsItem = generator.createCreateAccountsItem(keys_o, amounts)
>>> createAccountsFact = generator.createCreateAccountsFact(source_addr, [createAccountsItem])

>>> createAccounts = generator.createOperation(createAccountsFact, "")
>>> createAccounts.addFactSign(source_priv)
```

You must add new fact signature by addFactSign before creating seal or json files from an operation.

Then Operation.to_dict() and Operation.to_json(file_name) methods work correctly.

```python
>>> createAccounts.to_dict()
>>> createAccounts.to_json("create_account.json")
```

Then the result format will be like [this](example/create_accounts.json). (Each value is up to input arguments and time)


### Generate Key-Updater

Key-Updater literally supports to update source public key to something else.

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

### Generate Create-Documents

To generate an operation, you must prepare file-hash. Create-Document supports to create documents with setting signers who must sign them.

#### Usage

```python
>>> from mitumc.operation import Generator

>>> source_priv = "L5GTSKkRs9NPsXwYgACZdodNUJqCAWjz2BccuR4cAgxJumEZWjok:btc-priv-v0.0.1"
>>> source_addr = "GbymDFuVmJwP4bjjyYu4L6xgBfUmdceufrMDdn4x1oz:mca-v0.0.1"

>>> generator = Generator('mitum')

>>> createDocumentsItem = generator.createCreateDocumentsItem("abcdddd:mbhf-v0.0.1", 100, "user01", "title100", 1234, "MCC", [], ["user02"])

>>> createDocumentsFact = generator.createCreateDocumentsFact(source_addr, [createDocumentsItem])

>>> createDocuments = generator.createOperation(createDocumentsFact, "")
>>> createDocuments.addFactSign(source_prv)

>>> createDocuments.to_dict()
>>> createDocuments.to_json('create_documents.json')
```

### Generate Sign-Documents

To generate an operation, you must prepare owner and document id. Sign-Document supports to sign documents registered by 'mitum-data-blocksign'

#### Usage

```python
>>> from mitumc.operation import Generator

>>> source_priv = "L5GTSKkRs9NPsXwYgACZdodNUJqCAWjz2BccuR4cAgxJumEZWjok:btc-priv-v0.0.1"
>>> source_addr = "GbymDFuVmJwP4bjjyYu4L6xgBfUmdceufrMDdn4x1oz:mca-v0.0.1"

>>> generator = Generator('mitum')

>>> signDocumentsItem = generator.createSignDocumentsItem(source_addr, 0, "MCC")

>>> signDocumentsFact = generator.createSignDocumentsFact(source_addr, [signDocumentsItem])

>>> signDocuments = generator.createOperation(signDocumentsFact, "")
>>> signDocuments.addFactSign(source_prv)

>>> signDocuments.to_dict()
>>> signDocuments.to_json('sign_documents.json')
```

### Generate Transfer-Documents

To generate an operation, you must prepare owner and document id. Transfer-Document supports to transfer documents to other account.

#### Usage

```python
>>> from mitumc.operation import Generator

>>> source_priv = "L5GTSKkRs9NPsXwYgACZdodNUJqCAWjz2BccuR4cAgxJumEZWjok:btc-priv-v0.0.1"
>>> source_addr = "GbymDFuVmJwP4bjjyYu4L6xgBfUmdceufrMDdn4x1oz:mca-v0.0.1"
>>> target_addr = "ATDxH32CL7hdrpgLcvtNroNTF111V6wUJCK5JTa4f8Po:mca-v0.0.1"

>>> generator = Generator('mitum')

>>> transferDocumentsItem = generator.createTransferDocumentsItem(source_addr, target_addr, 0, "MCC")

>>> transferDocumentsFact = generator.createTransferDocumentsFact(source_addr, [transferDocumentsItem])

>>> transferDocuments = generator.createOperation(transferDocumentsFact, "")
>>> transferDocuments.addFactSign(source_prv)

>>> transferDocuments.to_dict()
>>> transferDocuments.to_json('transfer_documents.json')
```

## Generate New Seal

Supports you to generate a seal json file such that the seal is able to consist of several operations. Those operations can be any type 'mitum-py-util' provides.

### Prerequisite

To generate a seal, 'mitum-py-util' requires,

* 'signing key'
* 'a list of pre-constructed operations' not empty

Registration of 'signing key' is not neccessary.

### JSONParser

You can create a json file from generated seal object without 'JSONParser' class provided by 'mitumc'. However, I recommend to use 'JSONParser' for convenience.

Modules that 'JSONParser' supports are,

```python
>>> JSONParser.toJSONString(seal)
>>> JSONParser.generateFile(seal, fName)
```

A use-case of 'JSONParser' will be introduced in the next part.

### Usage

First of all, suppose that every operation is that generated by 'Generator'. (createAccounts, keyUpdater, Transfers)

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
$ ./mc seal send --network-id=$NETWORK_ID $SIGNING_KEY --seal=seal.json
```

* seal.json is your seal file.

## Sign Message

Sign message with btc, ether, stellar keypair.

'mitumc.key' module supports generate and get keypairs. You can get signature digest which contains a signature by signing with keypairs.

### Usage

#### Generate Keypair

```python
>>> from mitumc.key import getKeypair

>>> btckp = getKeypair('btc') # returns BTCKeyPair
>>> ethkp = getKeypair('ether') # returns ETHKeyPair
>>> stlkp = getKeypair('stellar') # returns StellarKeyPair

>>> btckp.privkey.key
5JDCaUK6NoD8vdUdmxptiKXGqgx7ngH3aL3c1FQ19jHLo9anwW3

>>> btckp.pubkey.key
wk4RnmibruceqbjcunJpAE9ufXVgpAHuvXXBBKQUvzas

>>> ethkp.privkey.key
7222d364be36e4f038270065a5c9f5c1dadf97a85ab14305f6580e243e224d8a

>>> ethkp.pubkey.key
049757460673bbd7d6e9904eb3554055614dce1d39aea623a07483065fb655d87d1797a0ce131ca8ae8bd8da20097a6cbc1c60b8246dc770907ef30a3dc78cdd9d

>>> stlkp.privkey.key
SCEKV2MWAZQCQGKYYTPVMOBR52CRFVROT4XGMOLVSSFYD5K7AM24L57T

>>> stlkp.pubkey.key
GBQRPKLCB7BTURVHA33LC5HKKXAOISMELEN6YYSDECKH4LSOS6YJCYCT
```

Note that 'mitumc.key' provides uncompressed btc key.

If you want to get compressed wif key, use 'BTCKeyPair.wifc'.

```python
>>> from mitumc.key import getKeypair

>>> btckp = getKeypair('btc')
>>> btckp.wifc
Kxxr6jYrjCxZyhzyKTQPFNkcuuLGxcMpN74VW6YXfXd8NXALHhDE
```

Of course, you can get any keypair with your known private key.

Note that it works with either hintless or hinted keys to generate keypairs.
(key-hint ex. btc-priv, ether-pub, etc...) 

```python
>>> from mitumc.key import to_btc_keypair, to_ether_keypair, to_stellar_keypair

# both work same
>>> btckp = to_btc_keypair("L2ddEkdgYVBkhtdN8HVXLZk5eAcdqXxecd17FDTobVeFfZNPk2ZD:btc-priv-v0.0.1")
>>> btckp = to_btc_keypair("L2ddEkdgYVBkhtdN8HVXLZk5eAcdqXxecd17FDTobVeFfZNPk2ZD") # returns BTCKeyPair

>>> ethkp = to_ether_keypair("013e56aca7cf88d95aa6535fb6c66f366d449a0380128e0eb656a863b45a5ad5:ether-priv-v0.0.1") # returns ETHKeyPair
>>> stlkp = to_stellar_keypair("SBZV72AJVXGARRY6BYXF5IPNQYWMGZJ5YVF6NIENEEATETDF6LGH4CLL:stellar-priv-v0.0.1") # returns StellarKeyPair
```

#### Sign Message

Each keypair supports 'sign' method that generates bytes format signature by signing bytes format message.

If you want to get signature for 'mitum-currency', use 'base58' to encode the signature.

```python
>>> from mitumc.key import getKeypair
>>> import base58

>>> msg = b'mitum'

>>> btckp = getKeypair('btc')
>>> sign = btckp.sign(msg)

>>> sign
b'0E\x02!\x00\xd4\xcb\xa3\x05\xec\x92-\xde\xcc\xb9;,\xf7k\x0bl\x8d\xf7@B\xaf\xf6 \x0f\xa5\xd1\x10]N1\xcc<\x02 \x119; lJ\x83\x1e\xdd\xfd\xce\x12vVK\x8aG\xae\xba\xe7\x03%\x98\xa5\x1b\'\x99"\xc2\xaf\xa5c'

>>> base58.b58encode(sign).decode()
AN1rKvtXAEWjt4KUGZxoZ8e8YMVuLPo6MqciW9En5DbA1w1FLp6NhGmMFCuAjVipRBibWDkiVLQYvp4PcTiVezqNv4GtUKx18
```

Omit ether/stellar keypair sign. (bcz same...)

## Add Fact Signature to Operation

With 'Signer' object in 'mitum-py-util', you can add new fact signature to operation json.

To add signatures, you must prepare 'network id' and 'signing key'.

### Usage

For example, suppose that you already have an implemented operation json file like below.

operation.json
```json
{
    "memo": "",
    "_hint": "mitum-currency-transfers-operation-v0.0.1",
    "fact": {
        "_hint": "mitum-currency-transfers-operation-fact-v0.0.1",
        "hash": "HdVp5vNCVcdnTA5H36cEfNsjjZAktpgBLdL66rgTqFVA",
        "token": "MjAyMS0wNi0xMFQwNzowMjo0MS45NzgyOTErMDA6MDA=",
        "sender": "GbymDFuVmJwP4bjjyYu4L6xgBfUmdceufrMDdn4x1oz:mca-v0.0.1",
        "items": [
            {
                "_hint": "mitum-currency-transfers-item-single-amount-v0.0.1",
                "receiver": "8dsqP9dUPKv3TjJg6DCKJ7NE7vsMx47Gc4VrseEcyXtt:mca-v0.0.1",
                "amounts": [
                    {
                        "_hint": "mitum-currency-amount-v0.0.1",
                        "amount": "100",
                        "currency": "MCC"
                    }
                ]
            }
        ]
    },
    "hash": "6KJQdbLvomAh2HmjVuqQbYEVvVMMrsMgJEsrwcRMiqCx",
    "fact_signs": [
        {
            "_hint": "base-fact-sign-v0.0.1",
            "signer": "rcrd3KA2wWNhKdAP8rHRzfRmgp91oR9mqopckyXRmCvG:btc-pub-v0.0.1",
            "signature": "AN1rKvt3cim48ETgzpEaXC5EiRJfcPhVtsK7bUTNB3f9c9152Px4enY3xh59e7EmCgmiwVvzk3tvkmTk7B3MA74E2f5gpqFzG",
            "signed_at": "2021-06-10T07:02:42.614946Z"
        }
    ]
}
```

#### Sign Operation

Use 'Signer.signOperation(#operation-file-path)' to add new fact signature to "fact_signs" key.

After adding a fact signature, operation hash will be changed.

```python
>>> import mitumc.operation as op
>>> signer = op.Signer('mitum', "L4qMcVKwQkqrnPPtEhj8idCQyvCN2zyG374i5oftGQfraJEP8iek:btc-priv-v0.0.1")

>>> # Signer.signOperation(#target)
>>> # #target must be a dictionary object or the path of opertaion json file
>>> newOperation = signer.signOperation('operation.json') # or an object itself instead of the path 'operation.json'
```

After signing, above operation must be like below.(Each value is up to input arguments and time)

```json
{
    "memo": "",
    "_hint": "mitum-currency-transfers-operation-v0.0.1",
    "fact": {
        "_hint": "mitum-currency-transfers-operation-fact-v0.0.1",
        "hash": "HdVp5vNCVcdnTA5H36cEfNsjjZAktpgBLdL66rgTqFVA",
        "token": "MjAyMS0wNi0xMFQwNzowMjo0MS45NzgyOTErMDA6MDA=",
        "sender": "GbymDFuVmJwP4bjjyYu4L6xgBfUmdceufrMDdn4x1oz:mca-v0.0.1",
        "items": [{
            "_hint": "mitum-currency-transfers-item-single-amount-v0.0.1",
            "receiver": "8dsqP9dUPKv3TjJg6DCKJ7NE7vsMx47Gc4VrseEcyXtt:mca-v0.0.1",
            "amounts": [{
                "_hint": "mitum-currency-amount-v0.0.1",
                "amount": "100",
                "currency": "MCC"
            }]
        }]
    },
    "fact_signs": [{
        "_hint": "base-fact-sign-v0.0.1",
        "signer": "rcrd3KA2wWNhKdAP8rHRzfRmgp91oR9mqopckyXRmCvG:btc-pub-v0.0.1",
        "signature": "AN1rKvt3cim48ETgzpEaXC5EiRJfcPhVtsK7bUTNB3f9c9152Px4enY3xh59e7EmCgmiwVvzk3tvkmTk7B3MA74E2f5gpqFzG",
        "signed_at": "2021-06-10T07:02:42.614946Z"
    }, {
        "_hint": "base-fact-sign-v0.0.1",
        "signer": "cnMJqt1Q7LXKqFAWprm6FBC7fRbWQeZhrymTavN11PKJ:btc-pub-v0.0.1",
        "signature": "AN1rKvt7VpVb76PXpKV2Znvixvo8bqmUJqha7WrkaTm3GKwZWfH8U2La13jJuPGvpcrbgLJqSYR5gHP2SwvtCM81NrtiBCW8a",
        "signed_at": "2021-07-20T08:24:29.163696Z"
    }],
    "hash": "DdwC2wAmvctrzCvnZSTu1xK2uKwNxNr9Y73xcHKLpqYb"
}
```

Signer class returns a dictionary object.

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
