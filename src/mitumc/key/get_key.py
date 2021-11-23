import mitumc.key.btc as btc
import mitumc.key.ether as ether
import mitumc.key.stellar as stellar

def getKeypair(k_type):
    """ Returns new KeyPair for k_type.
    - k_type: [ 'btc' | 'ether' | 'stellar' ]

    Returns:
        KeyPair: [ BTCKeyPair | ETHKeyPair | StellarKeyPair ]
        None if k_type is wrong.
    """
    if k_type == 'btc':
        return btc._get_keypair()
    elif k_type == 'ether':
        return ether._get_keypair()
    elif k_type == 'stellar':
        return stellar._get_keypair()
    else:
        return None