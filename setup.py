from setuptools import setup, find_packages

with open('README.md') as f:
    readme = f.read()

#with open('LICENSE') as f:
#    license = f.read()

setup(
    name='bitween',
    version='0.0.1',
    description='experimental XMPP/BT Client',
    long_description=readme,
    author='Jan Hartmann',
    url='https://github.com/puhoy/bitween',
    #license=license,
    packages=find_packages(exclude=('tests', 'docs')),
    test_suite="tests"
)