# mitum-py-util

'mitum-py-util' will introduce the usage of mitum-currency for python.

## Installation

Recommended requirements for 'mitum-py-util' are,

* python v3.9 or later.
* rlp v2.0.1
* base58 v2.1.0
* pybase64 v1.1.4
* ecdsa v0.13.3
* bitcoinaddress v0.1.5
* bitcoin-utils v0.4.11
* eth_keys v0.3.3
* stellar_sdk v3.3.2
* pytz v2021.1
* datetime v4.3

```
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

### Generate Create-Accounts 

To generate an operation, 'currency id' and 'initial amount' must be set. With source account, you can create and register new account of target public key.

#### Usage

```python
generate_create_accounts(network_id, source_private_key, source_address, amount, target_keys)
```

* 'amount' must be 2-length tuple in (big, currency id) format.
* 'target_keys' must be a list of 2-length tuple in (target_public_key, weight) format.

#### Example

```python
>>> from mitumc.operation import generate_create_accounts

>>> source_private_key = "L1oTaxcPztdqAU7ZzrHMWLnX2iUm6MhMW3RxT5YByiEpceDbUhPE-0112:0.0.1"
>>> source_address = "8AwAwFAaboopKDH7Nriq9Sq2eb2xjThMBFtWWCt3iebG-a000:0.0.1"
>>> target_public_key = "27LZo3wxW5T9VH5Da1La9bCSg1VfnaKtNvb3Gmg115N6X-0113:0.0.1"

>>> network_id = "mitum"

>>> amount = (100, "MCC")

>>> target_key = (target_public_key, 100)
>>> target_keys = list()
>>> target_keys.append(target_key)

>>> createAccounts = generate_create_accounts(network_id, source_private_key, source_address, amount, targets)
```

You can create json file of the operation by to_json(file_name) method.

```python
>>> createAccounts.to_json("create_account.json")
```

Then the result will be like [this](example/create_accounts.json)

### Generate Key-Updater

Key-Updater literally supports to update cource public key to something else.

#### Usage

```python
generate_key_updater(network_id, source_private_key, source_address, target_public_key, weight, currency_id)
```

* Every arguments must be single instance. (not tuple, list or somethine else...)

#### Example

```python
>>> from mitumc.operation import generate_key_updater

>>> source_private_key = "L1oTaxcPztdqAU7ZzrHMWLnX2iUm6MhMW3RxT5YByiEpceDbUhPE-0112:0.0.1"
>>> source_address = "8AwAwFAaboopKDH7Nriq9Sq2eb2xjThMBFtWWCt3iebG-a000:0.0.1"
>>> target_public_key = "27LZo3wxW5T9VH5Da1La9bCSg1VfnaKtNvb3Gmg115N6X-0113:0.0.1"

>>> network_id = "mitum"

>>> keyUpdater = generate_key_updater(network_id, source_private_key, source_address, target_public_key, 100, "MCC")
>>> keyUpdater.to_json("key_updater.json")
```

### Generate Transfers

To generate an operation, you must prepare target address, not public key. Transfers supports to send tokens to another account.

#### Usage

```python
generate_transfers(network_id, source_private_key, source_address, target_address, amount)
```

* 'amount' must be 2-length tuple in (big, currency id) format.

#### Example

```python
>>> from mitumc.operation import generate_transfers

>>> source_private_key = "L1oTaxcPztdqAU7ZzrHMWLnX2iUm6MhMW3RxT5YByiEpceDbUhPE-0112:0.0.1"
>>> source_address = "8AwAwFAaboopKDH7Nriq9Sq2eb2xjThMBFtWWCt3iebG-a000:0.0.1"
>>> target_address = "CHmkPR6GqTZfxrs1ptoWupsgvzkgvNdE7ZzhvimGUErg-a000:0.0.1"

>>> network_id = "mitum"

>>> amount = (100, "MCC")

>>> transfers = generate_transfers(network_id, source_private_key, source_address, target_address, amount)
>>> transfers.to_json("transfers.json")
```

## Generate New Seal

Supports you to generate a seal json file such that the seal is able to consist of several operations. Those operations can be any type 'mitum-py-util' provides.

### Prerequisite

To generate a seal, 'mitum-py-util' requires,

* 'signing key'
* 'a list of pre-constructed operations' not empty

Registration of 'signing key' is not neccessary.

### Usage

```python
generate_seal(file_name, network_id, signing_key, operations)
```

* 'signing key' must be a private key of 'mitum-currency' kepair.
* Every elements of operations list must be pre-constructed by 'generate_create_accounts', 'generate_key_updater', or 'generate_transfers'.

### Example

```python
>>> from mitumc.operation import generate_seal, generate_create_accounts, generate_key_updater, generate_transfers

>>> source_prv = "L5GTSKkRs9NPsXwYgACZdodNUJqCAWjz2BccuR4cAgxJumEZWjok-0112:0.0.1"
>>> source_addr = "8PdeEpvqfyL3uZFHRZG5PS3JngYUzFFUGPvCg29C2dBn-a000:0.0.1"

>>> ac1_prv = "SBGISVULOQA6BPEYF4OS2JGMBST7HYCBSL3TA2QRVGRNBMVWIZVE6336-0110:0.0.1"
>>> ac1_pub = "GBYLIBJYZP6ZIYPFGOZSXSAPMRDA6XXRKNSMOMRCKNV2YZ35DGRPEQ35-0111:0.0.1"
>>> ac2_addr = "8dsqP9dUPKv3TjJg6DCKJ7NE7vsMx47Gc4VrseEcyXtt-a000:0.0.1"
>>> ac3_pub = "GCV6WZ5U7HXFOXWTMLUXCG4PW3KP2YYTMAPZDE3IIVWQY7Q6SYPG63TZ-0111:0.0.1"

>>> createAccounts = generate_create_accounts("mitum", source_prv, source_addr, (100, "MCC"), [(ac1_pub, 100)])
>>> keyUpdater = generate_key_updater("mitum", ac1_prv, ac1_addr, ac3_pub, 100, "MCC")
>>> transfers = generate_transfers("mitum", source_prv, source_addr, ac2_addr, (100, "MCC"))

>>> operations = [createAccounts, keyUpdater, transfers]
>>> network_id = "mitum"

>>> generate_seal("seal.json", network_id, source_prv, operations)
```

Then the result will be like [this](example/seal.json).

## Send Seal to Network

Created seal json files will be used to send seals by 'mitum-currency'.

Use below command to send them to the target network. (See [mitum-currency](https://github.com/ProtoconNet/mitum-currency) for details)

```
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
>>>print(sha3_hash.hash)
```

The result will be,

```
$ python mitumc_hash.py
b'\xf7.\xd28\xfd\xc1+\xfc\x1d\xa9\xcdb9y\x8cF+RW4\x89)\x99\xcb\xdc\xf5\xbe\xf5\xa7J\xf2\x95'
Hdu7PqjA1p55GAcBiULmCAfzoksdwW1oSxaMH83kw9BJ
b'jf\x10J>\xb9O]\x14\xab}d,r\x88(B\xab\x9a\xb1x\x18\x04\xeb\x10!\x9f\xebY\xa5v"'
8ALUvxZ5Q1qQEsPUcHsoAzuzEp8Bm4HQpYqNNSafjDAR
```