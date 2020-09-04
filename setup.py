# OB - write your own commands.
#
#

from setuptools import setup

def read():
    return open("README.rst", "r").read()

setup(
    name='obdev',
    version='2',
    url='https://github.com/bthate/obdev',
    author='Bart Thate',
    author_email='bthate@dds.nl',
    description="OBDEV is the development environment for the OB package. OB is a event handler library and uses a timestamped JSON file backend to provide persistence. no copyright or LICENSE.",
    long_description=read(),
    license='Public Domain',
    zip_safe=True,
    packages=["ob"],
    namespace_packages=["ob"],
    classifiers=['Development Status :: 3 - Alpha',
                 'License :: Public Domain',
                 'Operating System :: Unix',
                 'Programming Language :: Python',
                 'Topic :: Utilities'
                ]
)
