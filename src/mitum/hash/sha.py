import hashlib

from mitum.common import Hash

# sha2 sha256 hashing
def sha256(b):
    sha2 = hashlib.sha256()
    sha2.update(b)
    return Hash(sha2.digest())


# sha3 sha256 hashing
def sum256(b):
    sha3 = hashlib.sha3_256()
    sha3.update(b)
    return Hash(sha3.digest())
