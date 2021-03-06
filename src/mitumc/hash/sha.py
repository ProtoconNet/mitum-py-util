import hashlib

from ..common import Hash


def sha256(b):
    assert isinstance(b, bytes), 'Input must be bytes object; sha256'

    sha2 = hashlib.sha256()
    sha2.update(b)

    return Hash(sha2.digest())

def sha3(b):
    assert isinstance(b, bytes), 'Input must be bytes object; sha3'
    
    sha3_256 = hashlib.sha3_256()
    sha3_256.update(b)

    return Hash(sha3_256.digest())
