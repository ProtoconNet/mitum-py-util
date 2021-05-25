from mitum.common import Hint, Int
from mitum.constant import VERSION
from mitum.hint import *
from mitum.key.base import Key, Keys, KeysBody, to_basekey

EXPECTED_KEYS_HASH = "HhgmNZQvabSfGSyKmXqQfTSJimjPTxsQ31B4Wd1UzFD5"

k = "hayB9VYA5KREe97duDwhtqvGgbRRzL4Y42y5WwrBZADB"
weight = 100
threshold = 100
currency = "MCC"

key = Key(
    Hint(BTC_PBLCKEY, VERSION),
    to_basekey(BTC_PBLCKEY, k),
    Int(weight),
)

key_list = list()
key_list.append(key)

keys_body = KeysBody(
    Hint(MC_KEYS, VERSION),
    Int(threshold),
    key_list,
)

keys = Keys(
    keys_body.generate_hash(),
    keys_body,
)

_keys_hash = keys.hash.hash == EXPECTED_KEYS_HASH
_fact_hash = False
_op_hash = False


print("[CHECK] KEYS HASH: " + str(_keys_hash))
if not _keys_hash:
    print("RESULT: " + keys.hash.hash)
    print("EXPECTED: " + EXPECTED_KEYS_HASH)
    print()

print("[CHECK] FACT HASH: ")
if not _fact_hash:
    pass

print("[CHECK] Operation HASH:" )
if not _op_hash:
    pass
