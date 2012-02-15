from setuptools import setup

from teamspeak3 import get_version

setup(
    name='teamspeak3',
    version=get_version(),
    url='http://bitbucket.org/latestrevision/python-teamspeak3/',
    description='Interact with teamspeak clients from Python',
    author='Adam Coddington',
    author_email='me@adamcoddington.net',
    classifiers=[
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Utilities',
    ],
    packages=['teamspeak3',],
    install_requires = []
)

