from distutils.core import setup

setup(
    name='chef',
    description='an interpreter for the esoteric programming language Chef',
    long_description='',
    version='0.1',
    author='Simon Liedtke',
    author_email='simonliedtke@posteo.de',
    url='http://pypi.python.org/pypi/chef',
    license='ISC',
    packages=[
        'chef',
        'chef.errors',
        'chef.tests',
    ],
    scripts=['bin/chef'],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Topic :: Software Development :: Interpreters',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.5',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7']
)
