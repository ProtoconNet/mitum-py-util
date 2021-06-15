import json

import base58
from mitumc.common import (Hint, Int, bconcat, getNewToken, iso8601TimeStamp,
                           parseAddress, parseISOtoUTC)
from mitumc.constant import THRESHOLDS, VERSION
from mitumc.hash import sha
from mitumc.hint import (BTC_PRIVKEY, ETHER_PRIVKEY, MC_ADDRESS, MC_AMOUNT, MC_CREATE_ACCOUNTS_MULTIPLE_AMOUNTS,
                         MC_CREATE_ACCOUNTS_OP, MC_CREATE_ACCOUNTS_OP_FACT,
                         MC_CREATE_ACCOUNTS_SINGLE_AMOUNT, MC_KEY, MC_KEYS,
                         MC_KEYUPDATER_OP, MC_KEYUPDATER_OP_FACT, MC_TRANSFERS_ITEM_MULTI_AMOUNTS,
                         MC_TRANSFERS_OP, MC_TRANSFERS_OP_FACT,
                         MC_TRNASFERS_ITEM_SINGLE_AMOUNT, SEAL,
                         STELLAR_PRIVKEY)
from mitumc.key.base import Key, Keys, KeysBody, to_basekey
from mitumc.key.btc import to_btc_keypair
from mitumc.key.ether import to_ether_keypair
from mitumc.key.stellar import to_stellar_keypair
from mitumc.operation.base import (Address, Amount, Memo, Operation,
                                   OperationBody)
from mitumc.operation.create_accounts import (CreateAccountsFact,
                                              CreateAccountsFactBody,
                                              CreateAccountsItem)
from mitumc.operation.key_updater import KeyUpdaterFact, KeyUpdaterFactBody
from mitumc.operation.transfers import (TransfersFact, TransfersFactBody,
                                        TransfersItem)


def _to_keys(ks, threshold):
    _keys = []

    for _key in ks:
        key, w = _key

        t, k = parseAddress(key)
        _keys.append(
            Key(
                Hint(MC_KEY, VERSION),
                to_basekey(t, k),
                Int(w),
            )
        )

    keys_body = KeysBody(
        Hint(MC_KEYS, VERSION),
        Int(threshold),
        _keys,
    )

    keys = Keys(
        keys_body.generate_hash(),
        keys_body,
    )

    return keys


def _to_amounts(amts):
    amounts = []

    for _amt in amts:
        amounts.append(
            Amount(
                Hint(MC_AMOUNT, VERSION),
                Int(_amt[0]),
                _amt[1],
            )
        )

    return amounts


class Generator(object):
    def __init__(self, net_id):
        self.net_id = net_id

    def set_id(self, _id):
        self.net_id = _id

    def createKeys(self, keys, threshold):
        return _to_keys(keys, threshold)

    def createAmounts(self, amts):
        return _to_amounts(amts)
    
    def createCreateAccountsItem(self, keys_o, amts):    
        _hint = MC_CREATE_ACCOUNTS_SINGLE_AMOUNT

        if len(amts) > 1:
            _hint = MC_CREATE_ACCOUNTS_MULTIPLE_AMOUNTS

        return CreateAccountsItem(Hint(_hint, VERSION), keys_o, amts)

    def createTransfersItem(self, receiver, amts):
        _hint = MC_TRNASFERS_ITEM_SINGLE_AMOUNT

        if len(amts) > 1:
            _hint = MC_TRANSFERS_ITEM_MULTI_AMOUNTS

        t, addr = parseAddress(receiver)
        _receiver = Address(Hint(t, VERSION), addr)

        return TransfersItem(Hint(_hint, VERSION), _receiver, amts)
    
    def createCreateAccountsFact(self, sender, items):
        t, addr = parseAddress(sender)
        _sender = Address(Hint(t, VERSION), addr)

        fact_body = CreateAccountsFactBody(
            Hint(MC_CREATE_ACCOUNTS_OP_FACT, VERSION),
            iso8601TimeStamp(),
            _sender,
            items,
        )

        return CreateAccountsFact(
            self.net_id,
            fact_body.generate_hash(),
            fact_body,
        )

    def createKeyUpdaterFact(self, target, cid, keys_o):
        t, addr = parseAddress(target)
        _target = Address(Hint(t, VERSION), addr)

        fact_body =  KeyUpdaterFactBody(
            Hint(MC_KEYUPDATER_OP_FACT, VERSION),
            iso8601TimeStamp(),
            _target,
            cid,
            keys_o,
        )

        return KeyUpdaterFact(
            self.net_id,
            fact_body.generate_hash(),
            fact_body,
        )

    def createTransfersFact(self, sender, items):
        t, addr = parseAddress(sender)
        _sender = Address(Hint(t, VERSION), addr)

        fact_body = TransfersFactBody(
            Hint(MC_TRANSFERS_OP_FACT, VERSION),
            iso8601TimeStamp(),
            _sender,
            items,
        )

        return TransfersFact(
            self.net_id,
            fact_body.generate_hash(),
            fact_body,
        )

    def createOperation(self, fact, memo):
        if fact.hint() == MC_CREATE_ACCOUNTS_OP_FACT:
            _type = MC_CREATE_ACCOUNTS_OP
        elif fact.hint() == MC_KEYUPDATER_OP_FACT:
            _type = MC_KEYUPDATER_OP
        elif fact.hint() == MC_TRANSFERS_OP_FACT:
            _type = MC_TRANSFERS_OP
        else:
            return None

        oper_body = OperationBody(
            Memo(memo),
            Hint(_type, VERSION),
            fact,
        )

        return Operation(oper_body)

    def createSeal(self, sk, opers):
        assert opers, 'Operation list is empty!'
        
        for op in opers:
            assert isinstance(op, Operation), 'Invalid operation'
            assert op.hash() != None, "Some Operation haven't signed"

        t, k = parseAddress(sk)

        if t == BTC_PRIVKEY:
            kp = to_btc_keypair(k)
        elif t == ETHER_PRIVKEY:
            kp = to_ether_keypair(k)
        elif t == STELLAR_PRIVKEY:
            kp = to_stellar_keypair(k)
        else:
            return None
        
        signed_at = iso8601TimeStamp()
        bsigned_at = parseISOtoUTC(signed_at).encode()

        bsigner = kp.public_key.hinted().encode()

        bopers = bytearray()
        for op in opers:
            bopers += op.hash().digest

        body_hash = sha.sum256(bconcat(bsigner, bsigned_at, bopers))
        signature = kp.sign(bconcat(body_hash.digest, self.net_id.encode()))
        hash = sha.sum256(bconcat(body_hash.digest, signature))

        seal = {}
        seal['_hint'] = Hint(SEAL, VERSION).hint
        seal['hash'] = hash.hash
        seal['body_hash'] = body_hash.hash
        seal['signer'] = kp.public_key.hinted()
        seal['signature'] = base58.b58encode(signature).decode()
        seal['signed_at'] = getNewToken(signed_at)

        operations = list()
        for op in opers:
            operations.append(op.to_dict())
        seal['operations'] = operations

        return seal


class JSONParser(object):
    def toJSONString(seal):
        return json.dumps(seal)
    
    def generateFile(seal, fname):
        with open(fname, 'w') as fp:
            json.dump(seal, fp)