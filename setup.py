from setuptools import setup, find_packages

setup(
    name             = 'mitumc',
    version          = '0.1',
    description      = 'mitum-currency python util',
    long_description = open('README.md').read(),
    author           = 'wyuinche',
    author_email     = 'wyuinche.mido@gmail.com',
    license          = "GPLv3",
    package_dir      = {'':'./src'},
    url              = "https://github.com/ProtoconNet/mitum-py-util",
    install_requires = [
        'rlp', 'base58', 'pybase64',
        'ecdsa', 'bitcoinaddress', 'bitcoin-utils',
        'eth_keys', 'stellar_sdk',
        'pytz', 'datetime'
    ],
    packages         = find_packages('./src', exclude=['test', 'test_run']),
    keywords         = ['mitum', 'mitum-currency', 'mitumc', 'mitum-currency python util'],
    python_requires  = '>=3', 
)