from setuptools import setup, find_packages

setup(
    name='envsecure',
    version='0.1.0',
    packages=find_packages(),
    install_requires=[
        'pycryptodome',
        'click',
    ],
    entry_points={
        'console_scripts': [
            'envsecure=envsecure.cli:cli',
        ],
    },
    author='Your Name',
    description='Encrypt and decrypt .env files securely for CI/CD pipelines',
    keywords='env encryption security aes cli',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
    ],
)
