from setuptools import setup, find_packages
import codecs
import os

VERSION = '0.0.1'
DESCRIPTION = 'A secure hashing algorithm'
LONG_DESCRIPTION = '''
This package allows people to use the Ultra Secure Hashing Algoritm to hash and store sensitive data; such as password, and emails. This was designed for my own personal use but I decided to let everyone have access to this incredibly useful tool to implement into their applications.

## Exampe usage
```python
import usha

print(usha.usha2048("hello"))
```

## Output
```
4f02db3568787a554f02e79668797ee5ef92e6c678817e8d6b9ee72476847ee44f879ba4687d52c84ecfc7c8645b61a0efdfe6d82fc536c64efce7b3e47
77a642af40346565362d94bc22746667f7ccd2ef307868c32829d6bc71328757c7165efd762b478853d944fcb22b7687d5ab4ebcce6972edffc646f01e5
06702167db2f4307888f7fec1c2ef8e676587576450ed9a71484235dc46a9327476e017ede0eaece36404cf2554ed2e516605efde56ed707c47764eeb86
bdaa734768452f0efd25db67482b9e50ae2e548426a79622fa2c740908569d80ef1a6b8886d5e96efdb26c678857dbdeed2c787ec5e6bcc4f01d9b5e45b
79634e9fe51468457be46fd1a6b677c03d454f9a2748678573dd2f4122788c855e95eee423b66c4b7ad56e81e73877037ee6ead807c636656edd6edb97b
0f44358e36b921f2576827b4d2ec1e3c294556ee3cf01e7c8283a7cde2bc3273656bc1ec5eae02741b52555cfebcf27b5f5a10ac56ede872f7724cec2eb
9f2767728476c6aeba87461815466d4ef0cd3c607173e02ee2e7a6944af6856f506732747d38c38bc8e3b685dd6e956f90df48707f7cd66ef6e6c474736
b5c300224748bf33d946ef317307372f6e2aefb268f9754f6a26ad723a876451eae6edda6c878435b4a2fa0273857857ce56e9727387404fee42ef86318
4b733e466ad6e6c67664eebd6bd226d876827dc4cec3076e685ae2916edd0694746350a40af51337bd33f6652eeea7384f705c56ef0326b237639c3f6fc
2e30778856ad26f8f25c87780f81b2ec11f1857515ae66eef9bc67031323b6fdf274674850e494a8323b466041e346f99674874833edeaecaa7c80b5edc
966e830707780426deeb9f2767728476c64c02e32f65f176d0ef0107b674254e952ea0e72698057ce52f0027368c777d652af9e72689757ec56e91c7187
8416ee66f0216f4776556d4
```
'''

# Setting up
setup(
    name="usha",
    version=VERSION,
    author="easternblock678",
    author_email="",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    install_requires=[],
    keywords=['python', 'hashing', 'algorithm', 'secure', 'hashing algorithm', 'ultra secure hashing algorithm', 'usha', 'usha-2048', 'secure hashing algorithm', 'free', 'ak'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)