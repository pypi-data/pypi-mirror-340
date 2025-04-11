from setuptools import setup

VERSION = '0.2.0'

setup(
    name='pram',
    version=VERSION,
    py_modules=['pram'],
    url='https://github.com/JiscDACT/pram',
    download_url='https://github.com/JiscDACT/pram/tarball/{}'.format(VERSION),
    license='MIT',
    author='Scott Wilson',
    author_email='scott.bradley.wilson@gmail.com',
    description='Python library for implementing post-randomisation method (PRAM) for '
                'disclosure control in synthetic data',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    install_requires=['pandas', 'numpy'],
    entry_points={
        'console_scripts': ['pram=pram:main'],
    },
    classifiers=[
        'Development Status :: 4 - Beta',
        'License :: OSI Approved :: MIT License',
        'Topic :: Scientific/Engineering :: Mathematics',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11'
    ]
)