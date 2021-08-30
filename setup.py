import pathlib
import re
import sys

from setuptools import find_packages, setup

try:
    from pip.req import parse_requirements
except ImportError:  # pip >= 10.0.0
    from pip._internal.req import parse_requirements


WORK_DIR = pathlib.Path(__file__).parent

if sys.version_info < (3, 7):
    raise RuntimeError('Python version must be >= 3.7')


def requirements(filename=None):
    if filename is None:
        filename = 'requirements.txt'

    file = WORK_DIR / filename

    install_reqs = parse_requirements(str(file), session='hack')
    return [str(ir.req) for ir in install_reqs]



setup(
    name='FastViberApi',
    version='0.1',
    description='Python Distribution Utilities',
    author='Worrik',
    requires_python='>=3.7',
    url='https://github.com/Worrik/FastViberApi',
    install_requires=requirements(),
    packages=['fast_viber_api'],
)