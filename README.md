# mitum-py-util

'mitum-py-util' will introduce the usage of [mitum-currency](https://github.com/ProtoconNet/mitum-currency) and [mitum-data-blocksign](https://github.com/ProtoconNet/mitum-data-blocksign) for python.

## Installation

Recommended requirements for 'mitum-py-util' is,

* python v3.9 or later.

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

## Index

||Title|
|---|---|
|1|[Generate Keypair](#generate-keypair)|
|2|[How to Use Generator](#how-to-use-generator)|
|2-1|[Support Operations](#support-operations)|
|2-2|[Get Account Address from Keys](#get-account-address-from-keys)|
|3|[Generate Currency Operations](#generate-currency-operations)|
|3-1|[Generate Create-Accounts](#generate-create-accounts)|
|3-2|[Generate Key-Updater](#generate-key-updater)|
|3-3|[Generate Transfers](#generate-transfers)|
|4|[Generate BlockSign Operations](#generate-blocksign-operations)|
|4-1|[Generate BlockSign Create-Documents](#generate-blocksign-create-documents)|
|4-2|[Generate BlockSign Sign-Documents](#generate-blocksign-sign-documents)|
|5|[Generate BlockCity Operations](#generate-blockcity-operations)|
|5-1|[Generate User Document](#generate-user-document)|
|5-2|[Generate Land Document](#generate-land-document)|
|5-3|[Generate Vote Document](#generate-vote-document)|
|5-4|[Generate History Document](#generate-history-document)|
|5-5|[Generate BlockCity Create-Documents](#generate-blockcity-create-documents)|
|5-6|[Generate BlockCity Update-Documents](#generate-blockCity-update-documents)|
|6|[Generate New Seal](#generate-new-seal)|
|7|[Send Seal to Network](#send-seal-to-network)|
|8|[Sign Message](#sign-message)|
|9|[Add Fact Signature to Operation](#add-fact-signature-to-operation)|
|10|[Hash Functions](#hash-functions)|

<br />

|Class|
|---|
|[Generator](#generator)|
|[JSONParser](#jsonparser)|
|[Signer](#sign-operation)|

<br />

|Appendix|
|---|
|[About Time Stamp](#about-time-stamp)|

## Generate Keypair

There are type suffixes for each key and address.

`private key -> mpr`
<br>
`public key -> mpu`
<br>
`address -> mca`

You can get a new keypair by `getNewKeypair`. Also, it is available to get a keypair from already known private key or seed, either.

```python
getNewKeypair()
getKeypairFromPrivateKey(key)
getKeypairFromSeed(seed)
```

#### Usage

```python
from mitumc.key import getNewKeypair, getKeypairFromPrivateKey, getKeypairFromSeed

# get new Keypair
kp = getNewKeypair() # returns BTCKeyPair
kp.privateKey # KzafpyGojcN44yme25UMGvZvKWdMuFv1SwEhsZn8iF8szUz16jskmpr
kp.publicKey # 24TbbrNYVngpPEdq6Zc5rD1PQSTGQpqwabB9nVmmonXjqmpu

# get Keypair from your private key
pkp = getKeypairFromPrivateKey("L2ddEkdgYVBkhtdN8HVXLZk5eAcdqXxecd17FDTobVeFfZNPk2ZDmpr")

# get Keypair from your seed
skp = getKeypairFromSeed("Thisisaseedforthisexample.len(seed)>=36.")
```

The length of string seed must be longer than or equal to 36.

## How to Use Generator

### Support Operations

'mitum-py-util' provides three operations of 'mitum-currency',

* `Create-Accounts` creates an account corresponding to any public key with a pre-registered account.
* `Key-Updater` updates the public key of the account to something else.
* `Transfers` transfers tokens from the account to another account.

'mitum-currency' supports various kinds of operations, but 'mitum-py-util' will provide these frequently used operations.

In addition, 'mitum-py-util' provides two operations of 'mitum-data-blocksign',

* `Create-Documents` creates an document with filehash.
* `Sign-Documents` signs the document.

And it supports 4 document types and two operations of 'mitum-blockcity',

* `User Document` about user data.
* `Land Document` about renting.
* `Vote Document` about voting.
* `History Document` about document histories.

* `Create-Documents` creates an document with id.
* `Update-Documents` updates the state of documents.

### Generator

`mitumc` package provides `Generator` class to generate operations.

1. Set `network id` for Generator.

```python
from mitumc import Generator

id = 'mitum'
generator = Generator(id)
```

2. For `mitum-currency`, use `Generator.currency`

```python
from mitumc import Generator

generator = Generator('mitum')
currencyGenerator = generator.currency
```

What `Generator.currency` supports are, 

```python
Generator.currency.key(key, weight)
Generator.currency.amount(amount, currencyId)
Generator.currency.createKeys(keys, threshold)
Generator.currency.createAmounts(amounts) 
Generator.currency.createCreateAccountsItem(keys, amounts)
Generator.currency.createTransfersItem(receiver, amoutns)
Generator.currency.createCreateAccountsFact(sender, items)
Generator.currency.createKeyUpdaterFact(target, cid, keys)
Generator.currency.createTransfersFact(sender, items)
```

3. For `mitum-data-blocksign`, use `Generator.blockSign`

```python
from mitumc import Generator

generator = Generator('mitum')
blockSignGenerator = generator.blockSign
```

What `Generator.blockSign` supports are,

```python
Generator.blockSign.createCreateDocumentsItem(filehash, did, signcode, title, size, cid, signers, signcodes)
Generator.blockSign.createSignDocumentsItem(owner, documentid, cid)
Generator.blockSign.createBlockSignFact(operation_type)
```

4. For `mitum-blockcity`, user `Generator.blockCity`

```python
from mitumc import Generator

generator = Generator('mitum')
blockCityGenerator = generator.blockCity
```

What `Generator.blockCity` supports are,

```python
Generator.blockCity.candidate(address, nickname, manifest, count)
Generator.blockCity.info(docType, documentId)
Generator.blockCity.userStatistics(hp, strength, agility, dexterity, charisma, intelligence, vital)

Generator.blockCity.userDocument(info, owner, gold, bankGold, userStatistics)
Generator.blockCity.landDocument(info, owner, address, area, renter, account, rentDate, period)
Generator.blockCity.voteDocument(info, owner, round, endVoteTime, candidates, bossName, account, termofoffice)
Generator.blockCity.historyDocument(info, owner, name, account, date, usage, application)

Generator.blockCity.createDocumentsItem(document, currencyId)
Generator.blockCity.updateDocumentsItem(document, currencyId)
Generator.blockCity.createCreateDocumentsFact(sender, items)
Generator.blockCity.createUpdateDocumentsFact(sender, items)
```

5. To create `Operation` and `Seal`, use `Generator.createOperation(fact, memo)` and `Generator.createSeal(signKey, operations)`

```python
Generator.createOperation(fact, memo)
Generator.createSeal(signKey, operations)
```

You can check use-cases of Generator in the next part.

### Get Account Address from Keys

It is available to calculate the address of the account by its keys.

In `mitum`, `account` consists of `threshold`, and `pairs of (key, weight)`.

The available range of each value is, `1 <= threshold, weight <= 100`.

Note that the sum of all weights of the account should be bigger than or equal to threshold.

To get address, use `mitumc.Generator.currency`.

#### Usage

```python
from mitumc import Generator

gn = Generator('mitum').currency

pub1 = "21nHZiHxhjwXtXXhPFzMvGyAAdCobmZeCC1bT1yLXAaw2mpu"
pub2 = "mZKEkm4BnFq6ynq98q4bCEcE4kZhzLSViPbCx8LDBXk2mpu"
pub3 = "dPBms4cH4t8tiH6uNbq37HrEWwgrrEZqHQwSbvqEBJ85mpu"

key1 = gn.key(pub1, 40)
key2 = gn.key(pub2, 40)
key3 = gn.key(pub3, 40)

keys = gn.createKeys([key1, key2, key3], 80)
address = keys.address # your address
```

In this example, it is available to sign an operation with only 2 keys because the sum of 2 keys is bigger than or equal to the account's threshold.

## Generate Currency Operations

* Create-Accounts
* Key-Update
* Transfers

### Generate Create-Accounts 

For new account, `currency id` and `initial amount` must be set. With source account, you can create and register new account of target public key.

When you use `Generator`, you must set `network id` before you create something.

#### Usage

```python
from mitumc import Generator

srcPriv = "L1V19fBjhnxNyfuXLWw6Y5mjFSixzdsZP4obkXEERskGQNwSgdm1mpr"
srcAddr = "5fbQg8K856KfvzPiGhzmBMb6WaL5AsugUnfutgmWECPbmca"
targetPub = "2177RF13ZZXpdE1wf7wu5f9CHKaA2zSyLW5dk18ExyJ84mpu"

generator = Generator('mitum')
gn = generator.currency

key = gn.key(targetPub, 100)
keys = gn.createKeys([key], 100)

amount = gn.amount(100, 'MCC')
amounts = gn.createAmounts([amount])

createAccountsItem = gn.createCreateAccountsItem(keys, amounts)
createAccountsFact = gn.createCreateAccountsFact(srcAddr, [createAccountsItem])

createAccounts = generator.createOperation(createAccountsFact, "")
createAccounts.addFactSign(srcPriv)
```

You must add new fact signature by addFactSign before creating seal or json files from an operation.

Then `Operation.dict()` and `Operation.json(file_name)` methods work correctly.

```python
Operation.dict()
Operation.json("create_account.json")
```

Then the result format will be like [this](example/create_accounts.json). (Each value is up to input arguments and time)


### Generate Key-Updater

`Key-Updater` literally supports to update source public key to something else.

#### Usage

```python
from mitumc import Generator

srcPriv = "L1V19fBjhnxNyfuXLWw6Y5mjFSixzdsZP4obkXEERskGQNwSgdm1mpr"
srcAddr = "5fbQg8K856KfvzPiGhzmBMb6WaL5AsugUnfutgmWECPbmca"
desPub = "2BqW3iy3bb9Z1fS21opL3z4da69K25d9zR5DM2CnSuNYxmpu"

generator = Generator('mitum')
gn = generator.currency

key = gn.key(desPub, 100)
keys = gn.createKeys([key], 100)

keyUpdaterFact = gn.createKeyUpdaterFact(srcAddr, keys, "MCC")

keyUpdater = generator.createOperation(keyUpdaterFact, "")
keyUpdater.addFactSign(srcPriv)
```

### Generate Transfers

To generate an operation, you must prepare target address, not public key. `Transfers` supports to send tokens to another account.

#### Usage

```python
from mitumc import Generator

srcPriv = "L1V19fBjhnxNyfuXLWw6Y5mjFSixzdsZP4obkXEERskGQNwSgdm1mpr"
srcAddr = "5fbQg8K856KfvzPiGhzmBMb6WaL5AsugUnfutgmWECPbmca"
desAddr = "D2KjoTG6yhE64jGQu7y2hUYPzRoJ2RDcnPsWrtLBDaPTmca"

generator = Generator('mitum')
gn = generator.currency

amount = gn.amount(100, 'MCC')
amounts = gn.createAmounts([amount])

transfersItem = gn.createTransfersItem(desAddr, amounts)
transfersFact = gn.createTransfersFact(srcAddr, [transfersItem])

transfers = generator.createOperation(transfersFact, "")
transfers.addFactSign(srcPriv)
```

## Generate BlockSign Operations

* Create-Documents
* Sign-Documents

### Generate BlockSign Create-Documents

To generate an operation, you must prepare `file-hash`. `Create-Document` supports to create documents with setting signers who must sign them.

#### Usage

```python
from mitumc import Generator
from mitumc.operation.blocksign import BLOCKSIGN_CREATE_DOCUMENTS

srcPriv = "KwsWqjb6stDe5x6cdN6Xz4aNiina5HK8SmWXSCc1LMXE252gTD39mpr"
srcAddr = "FB3m9zS9DWYLgRETYr5j5A8WCTk5QY6dHAjTpzkjyPvzmca"

generator = Generator('mitum')
gn = generator.blockSign

createDocumentsItem = gn.createCreateDocumentsItem("abcdddd~mbhf-v0.0.1", 100, "user01", "title100", 1234, "MCC", [], ["user02"])
createDocumentsFact = gn.createBlockSignFact(BLOCKSIGN_CREATE_DOCUMENTS, sourceAddr, [createDocumentsItem])

createDocuments = generator.createOperation(createDocumentsFact, "")
createDocuments.addFactSign(srcPriv)
```

### Generate BlockSign Sign-Documents

To generate an operation, you must prepare `owner` and `document id`. `Sign-Document` supports to sign documents registered by 'mitum-data-blocksign'

#### Usage

```python
from mitumc import Generator
from mitumc.operation.blocksign import BLOCKSIGN_SIGN_DOCUMENTS

srcPriv = "KwsWqjb6stDe5x6cdN6Xz4aNiina5HK8SmWXSCc1LMXE252gTD39mpr"
srcAddr = "FB3m9zS9DWYLgRETYr5j5A8WCTk5QY6dHAjTpzkjyPvzmca"

generator = Generator('mitum')
gn = generator.blockSign

signDocumentsItem = gn.createSignDocumentsItem(srcAddr, 0, "MCC")
signDocumentsFact = gn.createBlockSignFact(BLOCKSIGN_SIGN_DOCUMENTS, srcAddr, [signDocumentsItem])

signDocuments = generator.createOperation(signDocumentsFact, "")
signDocuments.addFactSign(srcPriv)
```

## Generate BlockCity Operations

* User Document
* Land Document
* Vote Document
* History Document

* Create-Documents
* Update-Documents

### Generate User Document

What you must prepare before generate a user document are,

* document id
* Each value in a user statistics
* document owner
* user's gold and bank gold

#### Usage

```py
from mitumc import Generator
from mitumc.operation.blockcity import DOCTYPE_USER_DATA

id = 'mitum'
generator = Generator(id)
gn = generator.blockCity

info = gn.info(DOCTYPE_USER_DATA, "4cui")
statistics = gn.userStatistics(1, 1, 1, 1, 1, 1, 1)
userDocument = gn.userDocument(info, "5KGBDDsmNXCa69kVAgRxDovu7JWxdsUxtAz7GncKxRfqmca", 10, 10, statistics)
```

If you wonder what value needs for each parameter, see [Generator](#generator).

### Generate Land Document

What you must prepare are,

* document id
* document owner
* address to rent
* area to rent
* renter who rent
* account who rent
* rent date and period

#### Usage

```py
from mitumc.operation.blockcity import DOCTYPE_LAND_DATA

# Omit steps to generate Generator.. same with user document
info = gn.info(DOCTYPE_LAND_DATA, "4cli")
landDocument = gn.landDocument(info, "5KGBDDsmNXCa69kVAgRxDovu7JWxdsUxtAz7GncKxRfqmca", "abcd", "city1", "foo", "Gu5xHjhos5WkjGo9jKmYMY7dwWWzbEGdQCs11QkyAhh8mca", "2021-10-22", 10)
```

If you wonder what value needs for each parameter, see [Generator](#generator).

### Generate Vote Document

What you must prepare are,

* voting round
* end time of voting
* candidates - address, manifest, nickname and count
* boss name
* account address
* termofoffice

#### Usage

```py
from mitumc.operation.blockcity import DOCTYPE_VOTE_DATA

# Omit steps to generate Generator.. same with user document
info = gn.info(DOCTYPE_VOTE_DATA, "4cvi")
c1 = gn.candidate("8sXvbEaGh1vfpSWSib7qiJQQeqxVJ5YQRPpceaa5rd9Ymca", "foo1", "", 1)
c2 = gn.candidate("Gu5xHjhos5WkjGo9jKmYMY7dwWWzbEGdQCs11QkyAhh8mca", "foo2", "", 2)
voteDocument = gn.voteDocument(info, "5KGBDDsmNXCa69kVAgRxDovu7JWxdsUxtAz7GncKxRfqmca", 1, "2022-02-22", [c1, c2], "foo", "Gu5xHjhos5WkjGo9jKmYMY7dwWWzbEGdQCs11QkyAhh8mca", "2022")
```

If you wonder what value needs for each parameter, see [Generator](#generator).

### Generate History Document

What you must prepare are,

* document id
* document owner
* name
* account
* date
* usage
* application

#### Usage

```py
from mitumc.operation.blockcity import DOCTYPE_HISTORY_DATA

# Omit steps to generate Generator.. same with user document
info = gn.info(DOCTYPE_HISTORY_DATA, "1000chi")
historyDocument = gn.historyDocument(info, "8iRVFAPiHKaeznfN3CmNjtFtjYSPMPKLuL6qkaJz8RLumca", "abcd", "8iRVFAPiHKaeznfN3CmNjtFtjYSPMPKLuL6qkaJz8RLumca", "2022-02-01T00:00:00.000+09:00", "bob", "foo")
```

If you wonder what value needs for each parameter, see [Generator](#generator).

### Generate BlockCity Create-Documents

To generate create-documents operation, you have to prepare,

* currency id for fees
* document object generated along the above instructions.
* sender's address and private key

#### Usage

```py
from mitumc import Generator

generator = Generator('mitum')
gn = generator.blockCity

# .. generate document

item = gn.createCreateDocumentsItem(document, "PEN")
fact = gn.createCreateDocumentsFact("5KGBDDsmNXCa69kVAgRxDovu7JWxdsUxtAz7GncKxRfqmca", [item])

oper = generator.createOperation(fact, "")
oper.addFactSign("Kz5gif6kskQA8HD6GeEjPse1LuqF8d3WFEauTSAuCwD1h94vboyAmpr")
```

See the start of [Generate BlockCity Operations](#generate-blockcity-operations) for `Document`.

See [Generator](#generator) for details.

### Generate BlockCity Update-Documents

To generate create-documents operation, you have to prepare,

* currency id for fees
* document object generated along the above instructions.
* sender's address and private key

#### Usage

```py
from mitumc import Generator

generator = Generator('mitum')
gn = generator.blockCity

# .. generate document

item = gn.createUpdateDocumentsItem(document, "PEN")
fact = gn.createUpdateDocumentsFact("5KGBDDsmNXCa69kVAgRxDovu7JWxdsUxtAz7GncKxRfqmca", [item])

oper = generator.createOperation(fact, "")
oper.addFactSign("Kz5gif6kskQA8HD6GeEjPse1LuqF8d3WFEauTSAuCwD1h94vboyAmpr")
```

See the start of [Generate BlockCity Operations](#generate-blockcity-operations) for `Document`.

See [Generator](#generator) for details.

## Generate New Seal

Supports you to generate a seal json file such that the seal is able to consist of several operations. Those operations can be any type 'mitum-py-util' provides.

### Prerequisite

To generate a seal, 'mitum-py-util' requires,

* `signing key`
* `a list of pre-constructed operations` which is not empty

Registration of `signing key` is not necessary.

### JSONParser

You can create a json file from generated seal object without `JSONParser` class provided by `mitumc`. However, I recommend to use `JSONParser` just for convenience.

Modules that `JSONParser` supports are,

```python
JSONParser.toJSONString(seal)
JSONParser.generateFile(seal, fName)
```

A use-case of `JSONParser` will be introduced in the next part.

### Usage

First of all, suppose that every operation is that generated by `Generator`.

```python
from mitumc import Generator, JSONParser

generator = Generator('mitum')

... omitted
''' Create each operation [createAccounts, keyUpdater, transfers] with generator. See above sections.
'''
...

signKey = "L1V19fBjhnxNyfuXLWw6Y5mjFSixzdsZP4obkXEERskGQNwSgdm1mpr"

operations = [createAccounts, keyUpdater, transfers]
seal = generator.createSeal(signKey, operations)

JSONParser.toJSONString(seal)
JSONParser.generateFile(seal, 'seal.json')
```

Then the result format of `JSONParser.generateFile()` will be like [this](example/seal.json).

## Send Seal to Network

Use `curl` to send operations and seal to the network.

```shell
~$ curl -X POST -H "Content-Type: application/json" -d @seal.json https://{mitum network address}/builder/send
```

* `seal.json` is your seal file.

## Sign Message

Sign message with mitum keypair.

`mitumc.key` module supports generate and get keypairs. You can get signature digest which contains a signature by signing with keypairs.

### Sign Message with Keypair

Each keypair supports `sign` method that generates bytes format signature by signing bytes format message.

If you want to get signature for 'mitum-currency', use `base58` to encode the signature.

#### Usage

```python
from mitumc.key import getNewKeypair
import base58

msg = b'mitum'

kp = getKeypair('btc')
signature = kp.sign(msg) # b'0E\x02!\x00\xd4\xcb\xa3\x05\xec\x92-\xde\xcc\xb9;,\xf7k\x0bl\x8d\xf7@B\xaf\xf6 \x0f\xa5\xd1\x10]N1\xcc<\x02 \x119; lJ\x83\x1e\xdd\xfd\xce\x12vVK\x8aG\xae\xba\xe7\x03%\x98\xa5\x1b\'\x99"\xc2\xaf\xa5c'

mitumSignature = base58.b58encode(sign).decode() # AN1rKvtXAEWjt4KUGZxoZ8e8YMVuLPo6MqciW9En5DbA1w1FLp6NhGmMFCuAjVipRBibWDkiVLQYvp4PcTiVezqNv4GtUKx18
```

## Add Fact Signature to Operation

With `Signer` object in 'mitum-py-util', you can add new fact signature to operation json.

To add signatures, you must prepare `network id` and `signing key`.

### Sign Operation

For example, suppose that you already have an implemented operation json file like below.

operation.json
```json
{
    "memo": "",
    "_hint": "mitum-currency-transfers-operation-v0.0.1",
    "fact": {
        "_hint": "mitum-currency-transfers-operation-fact-v0.0.1",
        "hash": "DDQ1pjXsPVoGV5iWRZN4RhKSJ9zZRzn21tXW6HdM1gEe",
        "token": "MjAyMS0xMi0yOFQwNDo0MzowMy4xNzY5ODIrMDA6MDA=",
        "sender": "5fbQg8K856KfvzPiGhzmBMb6WaL5AsugUnfutgmWECPbmca",
        "items": [{
            "_hint": "mitum-currency-transfers-item-single-amount-v0.0.1",
            "receiver": "D2KjoTG6yhE64jGQu7y2hUYPzRoJ2RDcnPsWrtLBDaPTmca",
            "amounts": [{
                "_hint": "mitum-currency-amount-v0.0.1",
                "amount": "100",
                "currency": "MCC"
            }]
        }]
    },
    "hash": "3Eu7dyVpKtnYVf2HurNjoHLRPe9znQR2xWEkFGFTq1F8",
    "fact_signs": [{
        "_hint": "base-fact-sign-v0.0.1",
        "signer": "wAYCFysPp8bXP8YnnDJNjJGQbj6m9cvnqQUGkchMC1xfmpu",
        "signature": "AN1rKvtWVjsrSuZvYpyqmCEjL5YXSw4P4jXMBbANHHmX1HY7ukw1dazdpFZTjAnhFBzt9Xq3woJHf5DCPTUGiA96LSvGBP4vz",
        "signed_at": "2021-12-28T04:43:03.190259Z"
    }]
}
```

Use `Signer.signOperation(filePath)` to add new fact signature to "fact_signs" key.

After adding a fact signature, operation hash will be changed.

```python
from mitumc import Signer, JSONParser

signer = Signer('mitum', 'L1V19fBjhnxNyfuXLWw6Y5mjFSixzdsZP4obkXEERskGQNwSgdm1mpr')
signed = signer.signOperation('operation.json')

JSONParser.generateFile(signed, 'signed.json')
```

After signing, above operation must be like below.

```json
{
    "memo": "",
    "_hint": "mitum-currency-transfers-operation-v0.0.1",
    "fact": {
        "_hint": "mitum-currency-transfers-operation-fact-v0.0.1",
        "hash": "DDQ1pjXsPVoGV5iWRZN4RhKSJ9zZRzn21tXW6HdM1gEe",
        "token": "MjAyMS0xMi0yOFQwNDo0MzowMy4xNzY5ODIrMDA6MDA=",
        "sender": "5fbQg8K856KfvzPiGhzmBMb6WaL5AsugUnfutgmWECPbmca",
        "items": [
            {
                "_hint": "mitum-currency-transfers-item-single-amount-v0.0.1",
                "receiver": "D2KjoTG6yhE64jGQu7y2hUYPzRoJ2RDcnPsWrtLBDaPTmca",
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
    "fact_signs": [
        {
            "_hint": "base-fact-sign-v0.0.1",
            "signer": "wAYCFysPp8bXP8YnnDJNjJGQbj6m9cvnqQUGkchMC1xfmpu",
            "signature": "AN1rKvtWVjsrSuZvYpyqmCEjL5YXSw4P4jXMBbANHHmX1HY7ukw1dazdpFZTjAnhFBzt9Xq3woJHf5DCPTUGiA96LSvGBP4vz",
            "signed_at": "2021-12-28T04:43:03.190259Z"
        },
        {
            "_hint": "base-fact-sign-v0.0.1",
            "signer": "wAYCFysPp8bXP8YnnDJNjJGQbj6m9cvnqQUGkchMC1xfmpu",
            "signature": "381yXYrVVevf9tqV2cTBAiKQYoGSm4tn5ZGsHB5U1nX7xxKGkW9qMiDhz7P5aLhAbif1bn7hehydHeWishoY8rTQP1Ze7xr9",
            "signed_at": "2021-12-28T07:33:06.475723Z"
        }
    ],
    "hash": "CAjj7KhVhwPbHToHQ1JFkP9DoBjYU9qq91Dq3XkLtvVe"
}
```

Signer class returns a dictionary object.

## Hash Functions

`mitumc.hash` supports sha256 and sha3 hashing.

#### Example

```python
from mitumc.hash import sha256, sha3

msg = b'mitum'
sha2_hash = sha256(msg)
sha3_hash = sha3(msg)

print(sha2_hash.digest)
print(sha2_hash.hash)
print(sha3_hash.digest)
print(sha3_hash.hash)
```

The result will be,

```sh
$ python mitumc_hash.py
b'\xf7.\xd28\xfd\xc1+\xfc\x1d\xa9\xcdb9y\x8cF+RW4\x89)\x99\xcb\xdc\xf5\xbe\xf5\xa7J\xf2\x95'
Hdu7PqjA1p55GAcBiULmCAfzoksdwW1oSxaMH83kw9BJ
b'jf\x10J>\xb9O]\x14\xab}d,r\x88(B\xab\x9a\xb1x\x18\x04\xeb\x10!\x9f\xebY\xa5v"'
8ALUvxZ5Q1qQEsPUcHsoAzuzEp8Bm4HQpYqNNSafjDAR
```

## Appendix

### __About Time Stamp__

#### __Expression of Time Stamp__

For blocks, seals, signatures and etc, mitum uses `yyyy-MM-dd HH:mm:ss.* +0000 UTC` expression and `yyyy-MM-ddTHH:mm:ss.*Z` as standard.

All other timezones are not allowed! You must use only +0000 timezone for mitum.

For example,

1. When converting timestamp to byte format for generating block/seal/fact_sign hash
    - converting the string `2021-11-16 01:53:30.518 +0000 UTC` to bytes format

2. When putting timestamp in block, seal, fact_sign or etc
    - converting the timestamp to `2021-11-16T01:53:30.518Z` and put it in json

To generate operation hash, mitum concatenates byte arrays of network id, fact hash and byte arrays of fact_signs.

And to generate the byte array of a fact_sign, mitum concatenates byte arrays of signer, signature digest and signed_at.

Be careful that the format of `signed_at` when converted to bytes is like `yyyy-MM-dd HH:mm:ss.* +0000 UTC` but it will be expressed as `yyyy-MM-ddTHH:mm:ss.*Z` when putted in json.

#### __How many decimal places to be expressed?__

There is one more thing to note.

First at all, you don't have to care about decimal points of second(ss.*) in timestamp.

Moreover, you can write timestamp without `.` and any number under `.`.

However, you should not put any unnecessary zeros(0) in the float expression of second(ss.*) when converting timestamp to bytes format.

For example,

1. `2021-11-16T01:53:30.518Z` is converted to `2021-11-16 01:53:30.518 +0000 UTC` without any change of the time itself.

2. `2021-11-16T01:53:30.510Z` must be converted to `2021-11-16 01:53:30.51 +0000 UTC` when generating hash.

3. `2021-11-16T01:53:30.000Z` must be converted to `2021-11-16T01:53:30 +0000 UTC` when generating hash.

Any timestamp with some unnecessary zeros putted in json doesn't affect to effectiveness of the block, seal, or operation. Just pay attention when convert the format.