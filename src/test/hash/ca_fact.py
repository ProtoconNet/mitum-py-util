import mitumc.hint as HINT
from mitumc.common import Hint, Int
from mitumc.constant import VERSION
from mitumc.key.base import BaseKey, Key, Keys, KeysBody
from mitumc.operation import Address, Amount
from mitumc.operation.create_accounts import (CreateAccountsFact,
                                             CreateAccountsFactBody,
                                             CreateAccountsItem)

EXPECTED_KEYS_HASH = "4UM4CN8MZNyv26TK84486CX5X8bu9EUYbsWz5ovRsp1M"
EXPECTED_FACT_HASH = "7QR9ffV19CHuYypAzmQfBnpB3HMLkdvcwzhj3MSEZwH7"

k = "rd89GxTnMP91bZ1VepbkBrvB77BSQyQbquEVBy2fN1tV"

single_key = Key(
    Hint(HINT.MC_KEY, VERSION),
    BaseKey(Hint(HINT.BTC_PBLCKEY, VERSION), k),
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
    "MjAyMS0wNS0xMlQwNzo1MTowNC40NDI0NTRa",
    Address(Hint(HINT.MC_ADDRESS, VERSION), "8PdeEpvqfyL3uZFHRZG5PS3JngYUzFFUGPvCg29C2dBn"),
    item_list,
)

fact = CreateAccountsFact(
    fact_body.generate_hash(),
    fact_body,
)

print('[CHECK] KEYS HASH: ' + str(EXPECTED_KEYS_HASH == keys.hash.hash))
print('[CHECK] FACT HASH: ' + str(EXPECTED_FACT_HASH == fact.hash.hash))
