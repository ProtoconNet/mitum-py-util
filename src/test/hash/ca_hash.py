import base58
import mitum.hint as HINT
from mitum.common import Hint, Int
from mitum.constant import VERSION
from mitum.key.base import BaseKey, Key, Keys, KeysBody
from mitum.operation.base import Address, Amount, FactSign, Memo
from mitum.operation.create_accounts import (CreateAccounts,
                                             CreateAccountsBody,
                                             CreateAccountsFact,
                                             CreateAccountsFactBody,
                                             CreateAccountsItem)

EXPECTED_KEYS_HASH = "5terLZQX4fTPpjmBsjPjvwBLMY78qRWhKZ6j1kEiDNeV"
EXPECTED_FACT_HASH = "3fUbmP26sMkqED7qAiBau5ZdEyUrscf6sZWJmxayeqN4"
EXPECTED_OP_HASH = "2RaYS4AkX9fnzFUoEdYSVgQNpcCmwwC2WKidfX5FiWmY"

SIGNATURE = "381yXZNahRQxzrGMLscyfCxUCp4XNpzDWDPxAfm8nqUwpzKEDxTFR8mFbqTnJVG39vRjrf28hEPKEnoAFXoFh6VAjBJgsJTG"

key = "skRdC6GGufQ5YLwEipjtdaL2Zsgkxo3YCjp1B6w5V4bD"
single_key = Key(
    Hint(HINT.MC_KEY, VERSION),
    BaseKey(Hint(HINT.BTC_PBLCKEY, VERSION), key),
    Int(100),
)
key_list = list()
key_list.append(single_key)

keys_body = KeysBody(
    Hint(HINT.MC_KEYS, VERSION),
    Int(100),
    key_list,
)

keys = Keys(
    keys_body.generate_hash(),
    keys_body,
)

single_amount = Amount(
    Hint(HINT.MC_AMOUNT, VERSION),
    Int(1000),
    "MCC",
)

amount_list = list()
amount_list.append(single_amount)

single_item = CreateAccountsItem(
    Hint(HINT.MC_CREATE_ACCOUNTS_SINGLE_AMOUNT, VERSION),
    keys,
    amount_list,
)

item_list = list()
item_list.append(single_item)

fact_body = CreateAccountsFactBody(
    Hint(HINT.MC_CREATE_ACCOUNTS_OP_FACT, VERSION),
    "2021-05-18T02:02:16.066837Z",
    Address(Hint(HINT.MC_ADDRESS, VERSION), "4UM4CN8MZNyv26TK84486CX5X8bu9EUYbsWz5ovRsp1M"),
    item_list,
)

fact = CreateAccountsFact(
    fact_body.generate_hash(),
    fact_body,
)

fact_sign = FactSign(
    Hint(HINT.BASE_FACT_SIGN, VERSION),
    BaseKey(Hint(HINT.BTC_PBLCKEY, VERSION), "rd89GxTnMP91bZ1VepbkBrvB77BSQyQbquEVBy2fN1tV"),
    base58.b58decode(SIGNATURE.encode()),
    "2021-05-18T02:02:16.067000+00:00",
)

memo = Memo("")

sg_list = list()
sg_list.append(fact_sign)

op_body = CreateAccountsBody(
    memo,
    Hint(HINT.MC_CREATE_ACCOUNTS_OP, VERSION),
    fact,
    sg_list,
)

op = CreateAccounts(
    op_body.generate_hash(),
    op_body,
)

_keys_hash = EXPECTED_KEYS_HASH == keys.hash.hash
_fact_hash = EXPECTED_FACT_HASH == fact.hash.hash
_op_hash = EXPECTED_OP_HASH == op.hash.hash

print("[CHECK] KEYS HASH: " + str(_keys_hash))
if not _keys_hash:
    print("RESULT: " + keys.hash.hash)
    print("EXPECTED: " + EXPECTED_KEYS_HASH)
    print()

print("[CHECK] FACT HASH: " + str(_fact_hash))
if not _fact_hash:
    print("RESULT: " + fact.hash.hash)
    print("EXPECTED: " + EXPECTED_FACT_HASH)

print("[CHECK] Operation HASH: " + str(_op_hash))
if not _op_hash:
    print("RESULT: " + op.hash.hash)
    print("EXPECTED: " + EXPECTED_OP_HASH)
