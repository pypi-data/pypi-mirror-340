from setuptools import find_packages, setup

setup(
    name='securedict',
    packages=find_packages(include=['securedict']),
    version='0.9.6',
    description='Encrypted dicts',
    author='J.DeKeyrel',
    license='MIT',
    install_requires=['cryptography','kubernetes'],
    setup_requires=['pytest-runner'],
    tests_require=['pytest'],
    test_suite='tests',
)