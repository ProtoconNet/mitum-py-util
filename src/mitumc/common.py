import datetime

import base58
import pytz


class Int(object):
    """ Contains big endian integer.

    Attributes:
        value (int): Integer by big endian byteorder
    """
    def __init__(self, value):
        self.value = value
    
    def tight_bytes(self):
        # Converts int to N length bytes by big endian
        n = abs(self.value)
        
        result = bytearray()
        while(n):
            result.append(n & 0xff)
            n = n >> 8
        
        return bytes(result[::-1])

    def to_bytes(self):
        # Converts int to 8 length bytes by big endian 
        n = int(self.value)
        count = 0

        result = bytearray()
        while(n):
            result.append(n & 0xff)
            n = n >> 8
            count += 1

        result =  result[::-1] + bytearray([0] * (8-count))
        return bytes(result)

    def little4_to_bytes(self):
        # Convert int to 4 length bytes by little endian
        n = int(self.value)
        count = 0

        result = bytearray()
        while(n):
            result.append(n & 0xff)
            n = n >> 8
            count += 1
        result = result + bytearray([0] * (4-count))
        return bytes(result)


class Hint(object):
    """ Contains type-hint and mitum-currency version.

    Attributes:
        h_type (str): type-hint
        h_ver  (str): mitum-currency version
    """
    def __init__(self, type, ver):
        self.h_type = type
        self.h_ver = ver
    
    @property
    def type(self):
        return self.h_type

    @property
    def hint(self):
        return self.h_type + ":" + self.h_ver


class Hash(object):
    """ Contains hash digest.

    Attributes:
        hs (binary): Hash digest in binary format
    """
    def __init__(self, hs):
        self.hs = hs

    @property
    def digest(self):
        # Returns digest of hash in binary format
        return self.hs

    @property
    def hash(self):
        # Returns base58 encoded hash in string format
        return base58.b58encode(self.digest).decode()


def iso8601TimeStamp():
    return str(datetime.datetime.now(tz=pytz.utc).isoformat())

def getNewToken(iso):
    return iso[:26] + 'Z'

def parseISOtoUTC(t):
    date, at, z = t[:10], t[11:23], t[26:29] + t[30:]
    return date + " " + at + " " + z + " " + "UTC"

def bconcat(*blist):
    """ Concatenates bytes type arguments.

    Args:
        *blist: Arguments to concatenate
    
    Returns:
        bytes: Concatenated bytes type instance
    """
    concated = bytearray()
    
    for i in blist:
        assert isinstance(i, bytes) or isinstance(i, bytearray), 'Arguments must be provided in bytes or bytearray format'
        concated += bytearray(i)
    
    return bytes(concated)

def parseAddress(addr):
    """ Seperates address(or key) into type-hint and hintless address(key).

    Args:
        addr (str): Hinted address(or key)
    
    Returns:
        type (str): Hint of address(or key)
        addr (str): Address(or key) without hint
    """
    assert isinstance(addr, str), 'Input must be provided in string format'
    assert '-' in addr, 'Invalid format of Address(or key)'

    idx = addr.index('-')
    type = addr[idx+1:idx+5]
    return type, addr[:idx]
