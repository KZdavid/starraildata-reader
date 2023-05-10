from setuptools import setup, find_packages

setup(
    name='starraildatareader',
    version='0.1.0',
    author='KZdavid',
    author_email='kzdavid@outlook.com',
    description='A package for reading data from Dimbreath/StarRailData',
    packages=find_packages(where='src'),
    package_dir={'': 'src'},
    include_package_data=True,
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3'
    ],
)