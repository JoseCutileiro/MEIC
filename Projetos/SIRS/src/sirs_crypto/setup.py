from setuptools import setup, find_packages

setup(
    name='sirs_crypto',
    version='0.1',
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'sirs-crypto = sirs_crypto.cli:main',
        ],
    },
)