from setuptools import setup, find_packages
import sys

#
# required eggs
#
install_requires = [
    'pyramid',
]

#
# eggs that you need if you're running a version of python lower than 2.7
#
if sys.version_info[:2] < (2, 7):
    install_requires.extend(['argparse>=1.2.1', 'unittest2>=0.5.1'])

#
# eggs you need for development, but not production
#
dev_extras = (
    'coverage>=3.5.2',
    'fabric>=1.4.3',
    'zest.releaser>=3.37',
)

setup(
    name='ott.wules',
    version='0.1.0',
    description='Open Transit Tools - Web Rules / Content Engine',
    url='https://trinet.trimet.org/itbugs/projects/example',
    namespace_packages=('ott',),
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=install_requires,
    extras_require=dict(dev=dev_extras)
)
