from mitumc.common import bconcat
from mitumc.constant import NETWORK_ID
from mitumc.key.btc import to_btc_keypair

EXPECTED_SIGNATURE = "381yXZNahRQxzrGMLscyfCxUCp4XNpzDWDPxAfm8nqUwpzKEDxTFR8mFbqTnJVG39vRjrf28hEPKEnoAFXoFh6VAjBJgsJTG"

FACT_HASH = b"'\x92\xa6\xbe\x15\xbcG\x9f6Dd\xe8B\xad5\x1d\xd0?\x8a\xd8\xc7B9`X\xb2\xbc\x9c\x8a@\x91-"
sk ="L1jPsE8Sjo5QerUHJUZNRqdH1ctxTWzc1ue8Zp2mtpieNwtCKsNZ"
signed_at = "2021-05-18T02:02:16.067775Z"

kp = to_btc_keypair(sk)
signature = kp.sign(bconcat(FACT_HASH, NETWORK_ID.encode()))

result = signature == EXPECTED_SIGNATURE

print("[CHECK] signature: " + str(result))
if not result:
    print("RESULT:   " + signature)
    print("EXPECTED: " + EXPECTED_SIGNATURE)
