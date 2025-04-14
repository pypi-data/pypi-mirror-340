from setuptools import setup, find_packages

setup(
    name='data_creator_for_algo_trade_go',
    version='0.1',
    packages=find_packages(),
    install_requires=[
        'pymssql',
        'pandas'
    ],
    author='Okan Uregen',
    description='SQL Server bağlantısı ve veri işleme yardımcı sınıfı',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    classifiers=[
        'Programming Language :: Python :: 3',
    ],
)
