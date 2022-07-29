from setuptools import setup, find_packages

setup(
    name             = 'mitumc',
    version          = '2.0.0-beta1',
    description      = 'mitum model python util',
    long_description = open('README.md').read(),
    author           = 'protocon',
    author_email     = 'contact@protocon.io',
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
