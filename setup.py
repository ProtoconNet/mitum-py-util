from setuptools import setup, find_packages

setup(
    name             = 'mitumc',
    version          = '1.0.0',
    description      = 'mitum model python util',
    long_description = open('README.md').read(),
    author           = 'wyuinche',
    author_email     = 'wyuinche.mido@gmail.com',
    license          = "GPLv3",
    package_dir      = {'':'./src'},
    url              = "https://github.com/ProtoconNet/mitum-py-util",
    install_requires = [
        'base58', 'pybase64',
        'ecdsa', 'bitcoinaddress', 'bitcoin-utils',
        'pytz', 'datetime'
    ],
    packages         = find_packages('./src', exclude=['test', 'test_run']),
    keywords         = ['mitum', 'mitum-currency', 'mitumc', 'mitum-data-blocksign', 'mitum-blockcity'],
    python_requires  = '>=3.9', 
)
