from setuptools import find_packages, setup

setup(
    name='datasourcelib',
    packages=find_packages(include=['datasourcelib']),
    version='0.9.7',
    description='Datasource library',
    author='J.DeKeyrel',
    license='MIT',
    install_requires=['arrow','pymongo','psycopg2-binary'],
    setup_requires=['pytest-runner'],
    tests_require=['pytest'],
    test_suite='tests',
)