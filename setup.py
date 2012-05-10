from setuptools import setup, find_packages
from setuptools.command.sdist import sdist

setup(
    name='ply',
    version='0.1',
    description='Patch Manager for Git',
    url='https://github.com/rconradharris/ply',
    license='MIT',
    author='Rick Harris',
    author_email='rconradharris@gmail.com',
    packages=find_packages(),
    classifiers=[
        'Development Status :: 4 - Beta',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python :: 2.6'
    ],
    install_requires=[],
    scripts=['bin/ply'])
