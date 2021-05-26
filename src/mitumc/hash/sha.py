import hashlib

from mitumc.common import Hash


def sha256(b):
    """ Returns sha2-sha256 hash for input.

    Args:
        b (bytes): Target to hash 

    Returns:
        Hash: Hash object for b
    """
    assert isinstance(b, bytes), 'Input must be provided in byte format'

    sha2 = hashlib.sha256()
    sha2.update(b)

    return Hash(sha2.digest())

def sum256(b):
    """ Returns sha3-sha256 hash for input.

    Args:
        b (bytes): Target to hash 

    Returns:
        Hash: Hash object for b
    """
    assert isinstance(b, bytes), 'Input must be provided in byte format'
    
    sha3 = hashlib.sha3_256()
    sha3.update(b)

    return Hash(sha3.digest())
