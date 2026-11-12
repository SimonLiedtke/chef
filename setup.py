from setuptools import setup

setup(
    name='chef',
    description='an interpreter for the esoteric programming language Chef',
    long_description='',
    version='0.1',
    author='Simon Liedtke',
    author_email='simonliedtke@posteo.de',
    url='http://pypi.python.org/pypi/chef',
    license='ISC',
    python_requires='>=3.9',
    packages=[
        'chef',
        'chef.errors',
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
        'Programming Language :: Python :: 3']
)
