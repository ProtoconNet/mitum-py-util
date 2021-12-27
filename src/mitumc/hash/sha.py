import hashlib

from mitumc.common import Hash


def sha256(b):
    assert isinstance(b, bytes), 'Input must be provided in byte format'

    sha2 = hashlib.sha256()
    sha2.update(b)

    return Hash(sha2.digest())

def sha3(b):
    assert isinstance(b, bytes), 'Input must be provided in byte format'
    
    sha3_256 = hashlib.sha3_256()
    sha3_256.update(b)

    return Hash(sha3_256.digest())
