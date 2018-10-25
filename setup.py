from setuptools import setup, find_packages
from os.path import join, dirname
import ldapoid

setup(
    name='ldapoid',
    classifiers=['Programming Language :: Python :: 2.7', ],
    version=ldapoid.__version__,
    author=ldapoid.__author__,
    author_email=ldapoid.__author_email__,
    packages=find_packages(),
    long_description=open(join(dirname(__file__), 'README.rst')).read(),
    include_package_data=True,
    install_requires=['ldap', 'python-ldap']
)