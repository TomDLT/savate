import setuptools  # noqa  # used with `python setup.py develop`
from distutils.core import setup

descr = """This is a personal collection of tools to automatically
           save stuff during work."""

setup(
    name='savoto',
    version='0.1',
    description=descr,
    long_description=open('README.md').read(),
    license='BSD (3-clause)',
    download_url='https://github.com/tomdlt/savoto.git',
    url='http://github.com/tomdlt/savoto',
    maintainer='Tom Dupre la Tour',
    maintainer_email='tom.dupre-la-tour@m4x.org',
    packages=[
        'savoto',
    ], )
