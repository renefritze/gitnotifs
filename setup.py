import sys
from distutils.core import setup

tests_require = ['nose-cov', 'nose', 'nosehtmloutput', 'rednose']

setup(
    name = 'gitnotifs',
    version = '0.1',
    author = 'Rene Milk',
    author_email = 'rene.milk@uni-muenster.de',
    package_dir = {'':'src'},
    packages = ['gitnotifs',],
    scripts = ['bin/%s'%n for n in [] ],
    url = 'http://renemilk.github.com/gitnotifs',
    description = 'notification scripts/module for git repositories',
    long_description = open('README.txt').read(),
    tests_require = tests_require,
    # running `setup.py sdist' gives a warning about this, but still
    # install_requires is the only thing that works with pip/easy_install...
    # we do not list pyqt here since pip can't seem to install it
    install_requires = ['xmpppy', 'GitPython', 'jinja2'] + tests_require,
    classifiers = ['Development Status :: 4 - Beta',
	'Intended Audience :: System Administrators',
	'Topic :: Software Development :: Version Control'],
    license = open('LICENSE.txt').read()
)
