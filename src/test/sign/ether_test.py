import base58
from mitum.common import bconcat
from mitum.constant import NETWORK_ID
from mitum.key.ether import to_ether_keypair

EXPECTED_SIGNATURE = "5BpRZ6QFEXgF3KCxnMcKqTVw8hqqjkva3ddYQurXkPqWeGB8kvvpBXTYyT2ztwFvhsLP8KrR7sU6wd1fq671naeycuvKV"

FACT_HASH = "CVdKhHkp1w3NCCE4FHm6kSCpaBD2stEoQSsGMtL65fsb"
sk = "0c8f898c2887db97f9648dcf29359cd6ec7a283dcf726450f9d29795abd8787d"
vk = "04b3b30bbc253769998dd30f3a73d44f62f64658c458f25d1a9c42b68e60dc1bbaff869938ecb05fb618ac6a62150382000d55c3ede7512536cfa1cb366f0bb7a4"


kp = to_ether_keypair(sk)
signature = kp.sign(bconcat(base58.b58decode(FACT_HASH.encode()), NETWORK_ID.encode()))

result = signature == EXPECTED_SIGNATURE

print("[CHECK] signature: " + str(result))
if not result:
    print("RESULT:   " + signature)
    print("EXPECTED: " + EXPECTED_SIGNATURE)








