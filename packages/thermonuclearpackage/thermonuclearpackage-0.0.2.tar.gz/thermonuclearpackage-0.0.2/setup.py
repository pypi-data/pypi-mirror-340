from setuptools import setup, find_packages

VERSION = '0.0.2'
DESCRIPTION = 'Thermonuclear package'
LONG_DESCRIPTION = 'allows you to blow up a target no problem'

setup(
    name='thermonuclearpackage',
    version=VERSION,
    author='Aditya Jain',
    author_email='aditya.jain22@imperial.ac.uk',
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    install_requires=[],
    keywords=['terrorism','hate crimes'],
    classifiers=[
            "Development Status :: 3 - Alpha",
            "Intended Audience :: Education",
            "Programming Language :: Python :: 2",
            "Programming Language :: Python :: 3",
            "Operating System :: MacOS :: MacOS X",
            "Operating System :: Microsoft :: Windows"
    ]
)