from setuptools import setup, find_packages

from pip.req import parse_requirements

# parse_requirements() returns generator of pip.req.InstallRequirement objects
install_reqs = parse_requirements("requirements.txt", session=False)

reqs = [str(ir.req) for ir in install_reqs]


with open('README.rst') as f:
    readme = f.read()

# with open('LICENSE') as f:
#    license = f.read()

setup(
    name='bitween',
    version='0.0.1',
    description='experimental XMPP/BT Client',
    long_description=readme,
    author='Jan Hartmann',
    url='https://github.com/puhoy/bitween',
    # license=license,
    packages=find_packages(exclude=('tests', 'docs')),
    test_suite="tests",
    entry_points={
        'console_scripts': [
            'bitweend=bitween.bitweend:main',
            'bitweenc=bitween.bitweenc:main'
        ]
    },
    install_requires=reqs
)
