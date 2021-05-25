import base58
from mitum.common import bconcat
from mitum.constant import NETWORK_ID
from mitum.key.stellar import to_stellar_keypair

EXPECTED_SIGNATURE =  "31LVjvhp3Dqn6swPjmJb9F9Dw8PZEoEZ6LnMVoJpRywYFUYvHcwS2bjBD1qRTCoDCLkex9djeRfmjeg3fMouDNrP"

FACT_HASH = "2QoCDXteT2gReh2kMfHjwsKCy4YwxaGFWzpRxP44yJQY"
sk = "SAZQGIZMDUIMHNKH7VVJKI2UJ3JWLE5YEKMKZHREPCX67QVRHJ4QHCTR"
vk = "GDZFR67XMCDURLCIGH3ACRD55B2NAXF3NYWW5TXEPDKHNDRGWT7TARRA"

signed_at = "2021-05-20T07:33:36.518295487Z"

kp = to_stellar_keypair(sk)
signature = kp.sign(bconcat(base58.b58decode(FACT_HASH.encode()), NETWORK_ID.encode()))

result = signature == EXPECTED_SIGNATURE

print("[CHECK] signature: " + str(result))
if not result:
    print("RESULT:   " + signature)
    print("EXPECTED: " + EXPECTED_SIGNATURE)
