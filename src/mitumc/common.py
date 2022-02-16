import datetime

import base58
import pytz

from .constant import VERSION
from .hint import (KEY_PRIVATE, KEY_PUBLIC, MBC_HISTORY_DATA, MC_ADDRESS,
                         MBC_USER_DATA, MBC_LAND_DATA, MBC_VOTE_DATA)


class Int(object):
    def __init__(self, value):
        self.value = value

    def tight(self):
        n = abs(self.value)

        result = bytearray()
        while(n):
            result.append(n & 0xff)
            n = n >> 8

        return bytes(result[::-1])

    def bytes(self):
        n = int(self.value)
        count = 0

        result = bytearray()
        while(n):
            result.append(n & 0xff)
            n = n >> 8
            count += 1

        result = result[::-1] + bytearray([0] * (8-count))
        return bytes(result)


class Hint(object):

    def __init__(self, type, ver):
        self.h_type = type
        self.h_ver = ver

    @property
    def type(self):
        return self.h_type

    @property
    def hint(self):
        return self.h_type + "-" + self.h_ver


class Hash(object):
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
    idx = iso.find('+')
    if idx == -1:
        print('Invalid iso time; getNewToken')
        exit(-1)
    return iso[:idx] + 'Z'


def parseISOtoUTC(iso):
    t = iso.find('T')
    z = iso.find('Z')
    parsedTime = ""

    if z < 0:
        z = iso.find('+')

    assert z > -1, "Invalid ISO type; parseISOtoUTC"

    _time = iso[t + 1: z]
    if len(_time) > 12:
        _time = _time[0: 12]

    dot = _time.find('.')
    if dot < 0:
        parsedTime = _time
    else:
        decimal = _time[9: len(_time)]
        idx = decimal.rfind('0')
        if idx < 0 or idx != len(decimal) - 1:
            parsedTime = _time
        else:
            startIdx = len(decimal) - 1
            for i in range(len(decimal) - 1, -1, -1):
                if decimal[i] == '0':
                    startIdx = i
                else:
                    break
            if startIdx == 0:
                parsedTime = _time[0: dot]
            else:
                parsedTime = _time[0: dot] + '.' + decimal[0: startIdx]

    date, z = iso[:t], "+0000 UTC"

    return date + " " + parsedTime + " " + z


def concatBytes(*bList):
    concatenated = bytearray()

    for i in bList:
        assert isinstance(i, bytes) or isinstance(
            i, bytearray), 'Arguments must be provided in bytes or bytearray format; concatBytes'
        concatenated += bytearray(i)

    return bytes(concatenated)


def parseType(typed):
    assert len(typed) > 3, 'Invalid typed string; parseType'

    raw = typed[:-3]
    _type = typed[-3:]

    assert _type == MC_ADDRESS or _type == KEY_PRIVATE or _type == KEY_PUBLIC, 'Invalid type of typed string; parseType'

    return raw, _type


def parseDocumentId(documentId):
    assert len(documentId) > 3, 'Invalid typed string; parseDocumentId'

    _id = documentId[:-3]
    suffix = documentId[-3:]

    assert suffix == MBC_USER_DATA or suffix == MBC_LAND_DATA or suffix == MBC_VOTE_DATA or suffix == MBC_HISTORY_DATA

    return _id, suffix

def _hint(hint):
    return Hint(hint, VERSION)
