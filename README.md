# mitum-py-util
__mitum-py-util__ introduces the use of [mitum-currency](https://github.com/ProtoconNet/mitum-currency), [mitum-document](https://github.com/ProtoconNet/mitum-document), and [mitum-currency-extension](https://github.com/ProtoconNet/mitum-currency-extension) for python.

All addresses and keys in the document are examples. Please use your exact address and key when you actually use this package. All values in this document are not reliable.

__For all examples in this document, we are not responsible for using incorrect values.__

## Installation

Recommended requirements for 'mitum-py-util' are as follows:

* python v3.9 or later.

```sh
$ python --version
Python 3.9.2

$ git clone https://github.com/ProtoconNet/mitum-py-util.git

$ cd mitum-py-util

$ python setup.py install
```

If `setup.py` is not working properly, use `requirements.txt` to install the required package before running `setup.py`.

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
|3-4|[Generate Create-Contract-Accounts](#generate-create-contract-accounts)|
|3-5|[Generate Withdraws](#generate-withdraws)|
|4|[Generate Document Operations](#generate-document-operations)|
|4-1|[Generate BlockSign Documents](#generate-blocksign-documents)|
|4-2|[Generate BlockCity Documents](#generate-blockcity-documents)|
|4-3|[Generate Create-Documents](#generate-create-documents)|
|4-4|[Generate Update-Documents](#generate-update-documents)|
|4-5|[Generate BlockSign Sign-Documents](#generate-blocksign-sign-documents)|
|5|[Generate Feefi Operations](#generate-feefi-operations)|
|5-1|[Generate Pool-Register](#generate-pool-register)|
|5-2|[Generate Pool-Policy-Updater](#generate-pool-policy-updater)|
|5-3|[Generate Pool-Deposits](#generate-pool-deposits)|
|5-4|[Generate Pool-Withdraw](#generate-pool-withdraw)|
|6|[Generate NFT Operations](#generate-nft-operations)|
|6-1|[Generate Collection-Reister](#generate-collection-register)|
|6-2|[Generate Collection-Policy-Updater](#generate-collection-policy-updater)|
|6-3|[Generate NFT Mint](#generate-nft-mint)|
|6-4|[Generate NFT Transfer](#generate-nft-transfer)|
|6-5|[Generate NFT Burn](#generate-nft-burn)|
|6-6|[Generate Approve](#generate-approve)|
|6-7|[Geneate Delegate](#generate-delegate)|
|6-8|[Generate NFT Sign](#generate-nft-sign)|
|7|[Generate New Seal](#generate-new-seal)|
|8|[Send Seal to Network](#send-seal-to-network)|
|9|[Sign Message](#sign-message)|
|10|[Add Fact Signature to Operation](#add-fact-signature-to-operation)|
|11|[Hash Functions](#hash-functions)|

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

There is a type suffix for each key and address.

`private key -> mpr`
<br>
`public key -> mpu`
<br>
`address -> mca`

A new keypair can be obtained through `getNewKeypair`. You can also import keypairs from a known private key or seed.

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

String seeds must be longer than or equal to 36.

## How to Use Generator

This section describes how to use the `Generator` and what you need to prepare to use it.

### Support Operations

__mitum-py-util__ provides three operations of __mitum-currency__.

* __create-accounts__ creates accounts corresponding to public keys with pre-registered accounts.
* __key-updater__ updates the public keys in your account to something else.
* __transfers__ transfers tokens from an account to another account.

__mitum-currency__ supports many types of operations, but the __mitum-py-util__ only provides frequently used operations.

In addition, __mitum-py-util__ provides two operations of __mitum-document__.

* __create-documents__ creates documents.
* __update-documents__ updates the state of the document.

Currently, the SDK supports two models, __blocksign__ and __blockcity__, which are implemented based on __mitum-document__.

__mitum-blocksign__ provides an additional operation called __sign-documents__.

The following document types are available for each model:

* Use only one document type named `blocksign` for __mitum blocksign__.
* There are four document types for __blockcity__: `user`, `land`, `vote` and `history`.

### Generator

The __mitumc__ package provides a `Generator` class for creating jobs.

1. Set the `network id` of the `Generator`.

```python
from mitumc import Generator

id = 'mitum'
generator = Generator(id)
```

2. For __mitum-currency__, use `Generator.currency`.

```python
from mitumc import Generator

generator = Generator('mitum')
currencyGenerator = generator.currency
```

`Generator.currency` supports:

```python
Generator.currency.key(key, weight) # 1 <= $weight <= 100
Generator.currency.amount(currencyId, amount) 
Generator.currency.keys(keys, threshold) # 1 <= $threshold <= 100
Generator.currency.amounts(amounts) 
Generator.currency.getCreateAccountsItem(keys, amounts)
Generator.currency.getTransfersItem(receiver, amounts)
Generator.currency.getCreateAccountsFact(sender, items)
Generator.currency.getKeyUpdaterFact(target, currencyId, keys)
Generator.currency.getTransfersFact(sender, items)

Generator.currency.extension.getCreateContractAccountsItem(keys, amounts)
Generator.currency.extension.getWithdrawsItem(target, amounts)
Generator.currency.extension.getCreateContractAccountsFact(sender, items)
Generator.currency.extension.getWithdrawsFact(sender, items)
```

3. For __mitum-document__, use `Generator.document`.

```python
from mitumc import Generator

generator = Generator('mitum')
documentGenerator = generator.document
```

`Generator.document` supports:

```python
Generator.document.getCreateDocumentsItem(document, currencyId)
Generator.document.getUpdateDocumentsItem(document, currencyId)
Generator.document.getCreateDocumentsFact(sender, items)
Generator.document.getUpdateDocumentsFact(sender, items)
```

Note that __create-documents__ and __update-documents__ in the __mitum-document__ are common tasks for __blocksign__ and __blockcity__.

The document helps you create items and facts for these operations.

4. To generate objects specific to __blocksign__, use `Generator.document.blocksign`.

```python
Generator.document.blocksign.user(address, signcode, signed)
Generator.document.blocksign.document(documentId, owner, fileHash, creator, title, size, signers)
Generator.document.blocksign.getSignDocumentsItem(documentId, owner, currencyId)
Generator.document.blocksign.getSignDocumentsFact(sender, items)
```

__sign-documents__ is provided only for __blocksign__.

Therefore, it is `Generator.document.blocksign` rather than `Generator.document` that supports __sign-documents__.

The output of `user(...)` is provided as `signer` of `creator` or `document`.

5. To generate objects specific to __blockcity__, use `Generator.document.blockcity`.

```python
Generator.document.blockcity.candidate(address, nickname, manifest, count)
Generator.document.blockcity.userStatistics(hp, strength, agility, dexterity, charisma intelligence, vital)

Generator.document.blockcity.userDocument(documentId, owner, gold, bankGold, userStatistics)
Generator.document.blockcity.landDocument(documentId, owner, address, area, renter, account, rentDate, period)
Generator.document.blockcity.voteDocument(documentId, owner, round, endTime, candidates, bossName, account, office)
Generator.document.blockcity.historyDocument(documentId, owner, name, account, date, usage, application)
```

6. To create `Operation` and `Seal`, use `Generator.getOperation(fact, memo)` and `Generator.getSeal(signKey, operations)`

```python
Generator.getOperation(fact, memo)
Generator.getSeal(signKey, operations)
```

Use cases of `Generator` can be found in the next part.

### Get Account Address from Keys

You can calculate the address of the account with the key.

In __mitum__, `account` consists of `threshold` and `(key, weight) pairs`.

The available range for each value is `1 <= threshold, weight <= 100`.

The sum of all weights in the account must be greater than or equal to the threshold.

To obtain an address, use `mitumc.Generator.currency`.

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

keys = gn.keys([key1, key2, key3], 80)
address = keys.address # your address
```

In this example, because the sum of the weights of the two keys is greater than or equal to the account threshold, you can sign the operations with only two keys.

## Generate Currency Operations

This part shows how to create an operation for __mitum-currency__.

### Generate Create-Accounts 

For new accounts, `public keys` and `initial amounts` must be set. You can use the source account to create and register a new account that consists of target public keys.

However, the source account must already be registered.

When using `Generator`, you must first set the `network id`.

#### Usage

```python
from mitumc import Generator

srcPriv = "L1V19fBjhnxNyfuXLWw6Y5mjFSixzdsZP4obkXEERskGQNwSgdm1mpr"
srcAddr = "5fbQg8K856KfvzPiGhzmBMb6WaL5AsugUnfutgmWECPbmca"
targetPub = "2177RF13ZZXpdE1wf7wu5f9CHKaA2zSyLW5dk18ExyJ84mpu"

generator = Generator('mitum')
gn = generator.currency

key = gn.key(targetPub, 100)
keys = gn.keys([key], 100)

amount = gn.amount('MCC', 100)
amounts = gn.amounts([amount])

createAccountsItem = gn.getCreateAccountsItem(keys, amounts)
createAccountsFact = gn.getCreateAccountsFact(srcAddr, [createAccountsItem])

createAccounts = generator.getOperation(createAccountsFact, "")
createAccounts.addFactSign(srcPriv)
```

You must add new fact signature by `addFactSign()` before creating seal or json files from an operation.

Then `Operation.dict()` and `Operation.json(file_name)` methods work correctly.

```python
Operation.dict()
Operation.json("create_account.json")
```

Then the output format is the same as [this](example/create_accounts.json). (Each value depends on the input argument and time.)


### Generate Key-Updater

__key-updater__ literally support updating public keys to something else.

#### Usage

```python
from mitumc import Generator

srcPriv = "L1V19fBjhnxNyfuXLWw6Y5mjFSixzdsZP4obkXEERskGQNwSgdm1mpr"
srcAddr = "5fbQg8K856KfvzPiGhzmBMb6WaL5AsugUnfutgmWECPbmca"
desPub = "2BqW3iy3bb9Z1fS21opL3z4da69K25d9zR5DM2CnSuNYxmpu"

generator = Generator('mitum')
gn = generator.currency

key = gn.key(desPub, 100)
keys = gn.keys([key], 100)

keyUpdaterFact = gn.getKeyUpdaterFact(srcAddr, keys, "MCC")

keyUpdater = generator.getOperation(keyUpdaterFact, "")
keyUpdater.addFactSign(srcPriv)
```

### Generate Transfers

To cerate an operation, you must prepare a target address, not a public key. __transfers__ supports sending tokens to other accounts.

#### Usage

```python
from mitumc import Generator

srcPriv = "L1V19fBjhnxNyfuXLWw6Y5mjFSixzdsZP4obkXEERskGQNwSgdm1mpr"
srcAddr = "5fbQg8K856KfvzPiGhzmBMb6WaL5AsugUnfutgmWECPbmca"
desAddr = "D2KjoTG6yhE64jGQu7y2hUYPzRoJ2RDcnPsWrtLBDaPTmca"

generator = Generator('mitum')
gn = generator.currency

amount = gn.amount('MCC', 100)
amounts = gn.getAmounts([amount])

transfersItem = gn.getTransfersItem(desAddr, amounts)
transfersFact = gn.getTransfersFact(srcAddr, [transfersItem])

transfers = generator.getOperation(transfersFact, "")
transfers.addFactSign(srcPriv)
```

### Generate Create-Contract-Accounts 

For new contract accounts, `public keys` and `initial amounts` must be set. You can use the source account to create and register a new account that consists of target public keys. The owner of the new contract account will be this source account.

Note that source account must be already registered one.

#### Usage

```python
from mitumc import Generator

srcPriv = "L1V19fBjhnxNyfuXLWw6Y5mjFSixzdsZP4obkXEERskGQNwSgdm1mpr"
srcAddr = "5fbQg8K856KfvzPiGhzmBMb6WaL5AsugUnfutgmWECPbmca"
targetPub = "2177RF13ZZXpdE1wf7wu5f9CHKaA2zSyLW5dk18ExyJ84mpu"

generator = Generator('mitum')
gn = generator.currency

key = gn.key(targetPub, 100)
keys = gn.keys([key], 100)

amount = gn.amount('MCC', 100)
amounts = gn.amounts([amount])

createContractAccountsItem = gn.extension.getCreateContractAccountsItem(keys, amounts)
createContractAccountsFact = gn.extension.getCreateContractAccountsFact(srcAddr, [createContractAccountsItem])

createContractAccounts = generator.getOperation(createContractAccountsFact, "")
createContractAccounts.addFactSign(srcPriv)
```

### Generate Withdraws

To create an operation, you must prepare the target contract account address. __withdraws__ supports withdrawal of tokens from contract accounts.

#### Usage

```python
from mitumc import Generator

srcPriv = "L1V19fBjhnxNyfuXLWw6Y5mjFSixzdsZP4obkXEERskGQNwSgdm1mpr"
srcAddr = "5fbQg8K856KfvzPiGhzmBMb6WaL5AsugUnfutgmWECPbmca"
desAddr = "D2KjoTG6yhE64jGQu7y2hUYPzRoJ2RDcnPsWrtLBDaPTmca"

generator = Generator('mitum')
gn = generator.currency

amount = gn.amount('MCC', 100)
amounts = gn.getAmounts([amount])

withdrawsItem = gn.extension.getWithdrawsItem(desAddr, amounts)
withdrawsFact = gn.extension.getWithdrawsFact(srcAddr, [transfersItem])

withdraws = generator.getOperation(withdrawsFact, "")
withdraws.addFactSign(srcPriv)
```

## Generate Document Operations

To create or update documents, you must prepare an available document object for each operation item.

For example, __blocksign__ supports one type of document with a hint called `mitum-blocksign-document-data`.

However, __blockcity__ supports four types of documents: __user/land/vote/history__ documents that use different hints than __blocksign__.

In other words, you must create a document that corresponds to the type of document you want.

First, we'll show you how to create documents by type.

### Generate BlockSign Documents

As mentioned above, __blocksign__ only uses documents of __blocksign__ type.

You must first prepare the `creator` and the `signer`.

Each is called a `user` for convenience.

You can create a `user` using `Generator.document.blocksign.user(address, signCode, signed)`.

Here's what you need to prepare to create a document:

* document id
* owner
* file hash
* creator - from `user`
* title
* file size
* a signer list - signers from `user`

All `document id`s in the __blocksign__ are followed by the suffix `sdi`.

#### Usage

```python
from mitumc import Generator

user1 = "FB3m9zS9DWYLgRETYr5j5A8WCTk5QY6dHAjTpzkjyPvzmca"
user2 = "D2KjoTG6yhE64jGQu7y2hUYPzRoJ2RDcnPsWrtLBDaPTmca"

gn = Generator('mitum').document.blocksign

creator = gn.user(user1, "signer01", True)
signer1 = gn.user(user1, "signer01", True)
signer2 = gn.user(user2, "signer02", False)

document = gn.document("bstest01sdi", user1, "fs:01", creator, "doc01", "1234", [signer1, signer2])
```

For more information about each argument in the example, see [Generator](#generator).

### Generate BlockCity Documents

The following document types are supported in __blockcity__:

* User Data
* Land Data
* Voting Data
* History Data

The `document id` for each document type has a unique suffix.

* user data: `cui`
* land data: `cli`
* vote data: `cvi`
* history data: `chi`

The documents are used only in __blockcity__.

For more information about each argument in the example, see [Generator](#generator).

#### User Document

Before you create a `user` document, you must prepare the following:

* document id
* Each value in a user statistics
* document owner
* user's gold and bank gold

```python
from mitumc import Generator

gn = Generator('mitum').document.blockcity

statistics = gn.userStatistics(1, 1, 1, 1, 1, 1, 1)
document = gn.userDocument("4cui", "5KGBDDsmNXCa69kVAgRxDovu7JWxdsUxtAz7GncKxRfqmca", 10, 10, statistics)
```

####  Land Document

Here's what you need to prepare.

* document id
* document owner
* address to rent
* area to rent
* renter who rent
* account who rent
* rent date and period

```python
from mitumc import Generator

gn = Generator('mitum').document.blockcity

document = gn.landDocument("4cli", "5KGBDDsmNXCa69kVAgRxDovu7JWxdsUxtAz7GncKxRfqmca", "abcd", "city1", "foo", "Gu5xHjhos5WkjGo9jKmYMY7dwWWzbEGdQCs11QkyAhh8mca", "2021-10-22", 10)
```

### Vote Document

Here's what you need to prepare.

* voting round
* end time of voting
* candidates - address, manifest, nickname and count
* boss name
* account address
* termofoffice

```py
from mitumc import Generator

gn = Generator('mitum').document.blockcity

c1 = gn.candidate("8sXvbEaGh1vfpSWSib7qiJQQeqxVJ5YQRPpceaa5rd9Ymca", "foo1", "", 1)
c2 = gn.candidate("Gu5xHjhos5WkjGo9jKmYMY7dwWWzbEGdQCs11QkyAhh8mca", "foo2", "", 2)
document = gn.voteDocument("4cvi", "5KGBDDsmNXCa69kVAgRxDovu7JWxdsUxtAz7GncKxRfqmca", 1, "2022-02-22", [c1, c2], "foo", "Gu5xHjhos5WkjGo9jKmYMY7dwWWzbEGdQCs11QkyAhh8mca", "2022")
```

### Generate History Document

Here's what you need to prepare.

* document id
* document owner
* name
* account
* date
* usage
* application

```py
from mitumc import Generator

gn = Generator('mitum').document.blockcity

document = gn.historyDocument("4chi", "8iRVFAPiHKaeznfN3CmNjtFtjYSPMPKLuL6qkaJz8RLumca", "abcd", "8iRVFAPiHKaeznfN3CmNjtFtjYSPMPKLuL6qkaJz8RLumca", "2022-02-01T00:00:00.000+09:00", "bob", "foo")
```

### Generate Create-Documents

All models based on __mitum-document__ use operation as __create-documents__ and __update-documents__ by default.

This section will show you how to create documents and update documents for documents created in the previous part.

Go to the previous part for document creation.

To create a __create-documents__ operation, you must prepare the following:

* currency id for fees
* document
* sender's address and private key

#### Usage

```py
from mitumc import Generator

generator = Generator('mitum')
gn = generator.document

# .. generate document

item = gn.getCreateDocumentsItem(document, "PEN")
fact = gn.getCreateDocumentsFact("5KGBDDsmNXCa69kVAgRxDovu7JWxdsUxtAz7GncKxRfqmca", [item])

oper = generator.getOperation(fact, "")
oper.addFactSign("Kz5gif6kskQA8HD6GeEjPse1LuqF8d3WFEauTSAuCwD1h94vboyAmpr")
```

For `Document`, see the beginning of [Generate Document Operations](#generate-document-operations).

For more information, see [Generator](#generator).

### Generate Update-Documents

To create a __update-documents__ operation, you must prepare the following:

* currency id for fees
* document
* sender's address and private key

#### Usage

```py
from mitumc import Generator

generator = Generator('mitum')
gn = generator.document

# .. generate document

item = gn.getUpdateDocumentsItem(document, "PEN")
fact = gn.getUpdateDocumentsFact("5KGBDDsmNXCa69kVAgRxDovu7JWxdsUxtAz7GncKxRfqmca", [item])

oper = generator.getOperation(fact, "")
oper.addFactSign("Kz5gif6kskQA8HD6GeEjPse1LuqF8d3WFEauTSAuCwD1h94vboyAmpr")
```

For `Document`, see the beginning of [Generate Document Operations](#generate-document-operations).

For more information, see [Generator](#generator).

### Generate BlockSign Sign-Documents

As mentioned above, the __sign-documents__ operation is used only for __blocksign__.

Therefore, you must use the generator, `Generator.document.blocksign`, specific to  __blocksign__, to create items and facts for __sign-documents__.

To create an item for the __sign-document__, you must prepare the following:

* document id
* owner's address
* currency id for fee

You do not need to prepare a document for __sign-document__. Only `document id` is required.

#### Usage

```python
from mitumc import Generator

gn = Generator('mitum'); # Generator({networkId})

item = gn.document.blocksign.getSignDocumentsItem("4000sdi", "5KGBDDsmNXCa69kVAgRxDovu7JWxdsUxtAz7GncKxRfqmca", "PEN")
fact = gn.document.blocksign.getSignDocumentsFact("Gu5xHjhos5WkjGo9jKmYMY7dwWWzbEGdQCs11QkyAhh8mca", [item])

operation = gn.getOperation(fact, "")
operation.addSign("Kz5gif6kskQA8HD6GeEjPse1LuqF8d3WFEauTSAuCwD1h94vboyAmpr")
```

See [Generator](#generator) for details.

## Generate Feefi Operations

This part shows how to generate operations for __mitum-feefi__.

### Generate Pool-Register

__pool-register__ supports registering `pool` in a contract account.

#### Usage

```py
from mitumc import Generator

gn = Generator('mitum'); # Generator({networkId})

fee = gn.currency.amount("MCC", 1)
fact = gn.feefi.getPoolRegisterFact("CkiVJAwUhnhUWmPJcFCJrFSM7Y6jjLCdPMu2smEic2dTmca", "4rRNULRfGFLPTfZrhFzGqvbQ2cweiJuEZFNqrsMA353hmca", fee, "PEN", "AAA", "MCC")

operation = gn.getOperation(fact, "")
operation.addFactSign("KxE8Mq8TFfaDZ3d68uQmYKALhzFuZYGGb2UjwjtCsrhB7eSRmtnompr")
```

### Generate Pool-Policy-Updater

__pool-policy-updater__ supports updating registered pool policies.

#### Usage

```py
from mitumc import Generator

gn = Generator('mitum'); # Generator({networkId})

fee = gn.currency.amount("MCC", 10)
fact = gn.feefi.getPoolPolicyUpdaterFact("CkiVJAwUhnhUWmPJcFCJrFSM7Y6jjLCdPMu2smEic2dTmca", "4rRNULRfGFLPTfZrhFzGqvbQ2cweiJuEZFNqrsMA353hmca", fee, "PEN", "MCC")

operation = gn.getOperation(fact, "")
operation.addFactSign("KxE8Mq8TFfaDZ3d68uQmYKALhzFuZYGGb2UjwjtCsrhB7eSRmtnompr")
```

### Generate Pool-Deposits

__pool-deposits__ supports depositing amounts into the pool.

#### Usage

```py
from mitumc import Generator

gn = Generator('mitum'); # Generator({networkId})

amount = gn.currency.amount("PEN", 10)
fact = gn.feefi.getPoolDepositsFact("CkiVJAwUhnhUWmPJcFCJrFSM7Y6jjLCdPMu2smEic2dTmca", "4rRNULRfGFLPTfZrhFzGqvbQ2cweiJuEZFNqrsMA353hmca", "PEN", amount)

operation = gn.getOperation(fact, "")
operationaddFactSign("KxE8Mq8TFfaDZ3d68uQmYKALhzFuZYGGb2UjwjtCsrhB7eSRmtnompr")
```

### Generate Pool-Withdraw

__pool-withdraw__ supports withdrawing amounts from the pool.

#### Usage

```py
from mitumc import Generator

gn = Generator('mitum'); # Generator({networkId})

amounts = [gn.currency.amount("PEN", 1)]
fact = gn.feefi.getPoolWithdrawFact("CkiVJAwUhnhUWmPJcFCJrFSM7Y6jjLCdPMu2smEic2dTmca", "4rRNULRfGFLPTfZrhFzGqvbQ2cweiJuEZFNqrsMA353hmca", "PEN", amounts)

operation = gn.getOperation(fact, "")
operation.addFactSign("KxE8Mq8TFfaDZ3d68uQmYKALhzFuZYGGb2UjwjtCsrhB7eSRmtnompr")
```

## Generate NFT Operations

This part shows how to generate operations for __mitum-nft__.

### Generate Collection-Register

__collection-register__ supports the registration of `collection` in the contract account.

#### Usage

```py
```

### Generate Collection-Policy-Updater

__collection-policy-updater__ supports updating collection policies.


#### Usage

```py

```

### Generate NFT Mint

__mint__ supports the registration of a new nft in the collection.

#### Usage

This example shows how to create an operation when both the creator and copyrighter are the same account as minting nft.
Actually, any general account can be a creator and a copyrighter.

```py
```

### Generate NFT Transfer

__transfer__ supports the transfer of nft.

#### Usage

```py
```

### Generate NFT Burn

__burn__ supports nft burning.

#### Usage

```py
```

### Generate Approve

__approve__ supports delegation of authority for specific nft ownership changes.

#### Usage

```py
```

### Generate Delegate

__delegation__ supports delegating the authority to change ownership of all nfts held by one general account for a collection.

#### Usage

```py
```

### Generate NFT Sign

__sign__ supports signing in nft as a creator or copyrighter.

#### Usage

```py
```

## Generate New Seal

You can create a json file for a `seal` that consists of multiple operations. Any type of operation provided by __mitum-py-util__ is available.

### Prerequisite

To create a `seal`, __mitum-py-util__ requires the following:

* `signing key`
* `a list of pre-constructed operations` which is not empty

The signature key(private key generated by mitum) does not need to be registered.

### JSONParser

Even without the `JSONParser` class provided by `mitumc`, you can create a json file of `seal` objects created through a package embedded in javascript. However, for convenience, I recommend using `JSONParser`.

The modules supported by `JSONParser` are as follows:

```python
JSONParser.toString(seal)
JSONParser.toFile(seal, fName)
```

The next part introduces the use cases of `JSONParser`.

### Usage

Let's first assume that all operations are jobs created by the `Generator`.

```python
from mitumc import Generator, JSONParser

generator = Generator('mitum')

... omitted
''' Create each operation [createAccounts, keyUpdater, transfers] with generator. See above sections.
'''
...

signKey = "L1V19fBjhnxNyfuXLWw6Y5mjFSixzdsZP4obkXEERskGQNwSgdm1mpr"

operations = [createAccounts, keyUpdater, transfers]
seal = generator.getSeal(signKey, operations)

JSONParser.toString(seal)
JSONParser.toFile(seal, 'seal.json')
```

The output format of `JSONParser.toFile(...)` is the same as [this](example/seal.json).

## Send Seal to Network

Use `curl` to send operations and seals to the network.

```shell
~$ curl -X POST -H "Content-Type: application/json" -d @seal.json https://{mitum network address}/builder/send
```

* `seal.json` becomes your seal json file.

## Sign Message

Sign the message with a mitum keypair.

`mitumc.key` module supports keypair generation and import. You can obtain signature digest by signing with a keypair.

### Sign Message with Keypair

Each keypair supports the `sign` method, which generates a byte-type signature by signing a byte-type message.

To obtain a signature for __mitum__, encode the signature using `base58`.

#### Usage

```python
from mitumc.key import getNewKeypair
import base58

msg = b'mitum'

kp = getNewKeypair()
signature = kp.sign(msg) # b'0E\x02!\x00\xd4\xcb\xa3\x05\xec\x92-\xde\xcc\xb9;,\xf7k\x0bl\x8d\xf7@B\xaf\xf6 \x0f\xa5\xd1\x10]N1\xcc<\x02 \x119; lJ\x83\x1e\xdd\xfd\xce\x12vVK\x8aG\xae\xba\xe7\x03%\x98\xa5\x1b\'\x99"\xc2\xaf\xa5c'

mitumSignature = base58.b58encode(sign).decode() # AN1rKvtXAEWjt4KUGZxoZ8e8YMVuLPo6MqciW9En5DbA1w1FLp6NhGmMFCuAjVipRBibWDkiVLQYvp4PcTiVezqNv4GtUKx18
```

## Add Fact Signature to Operation

WYou can add a new fact signature to operation json using the `Signer` object in __mitum-py-util__.

To add a signature, you must prepare a `network id` and a `signature key`.

### Sign Operation

For example, suppose you have an operation json file that has already been implemented, as shown below.

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

Use `Signer.signOperation(filePath)` to add a new fact signature to the `fact_signs` array.

The __operation hash__ changes after adding a fact signature.

```python
from mitumc import Signer, JSONParser

signer = Signer('mitum', 'L1V19fBjhnxNyfuXLWw6Y5mjFSixzdsZP4obkXEERskGQNwSgdm1mpr')
signed = signer.signOperation('operation.json')

JSONParser.toFile(signed, 'signed.json')
```

After signing, the above operation must be changed as follows.

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

`Signer` class returns a dictionary object.

## Hash Functions

`mitum.hash` supports `sha256` and `sha3` hashing.

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

The results are as follows:

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