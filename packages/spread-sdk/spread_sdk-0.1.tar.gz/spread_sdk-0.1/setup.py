
from setuptools import setup

setup(
    name='spread-sdk',
    version='0.1',
    py_modules=['spread_sdk'],
    install_requires=['websockets', 'requests'],
    author='TechOps',
    author_email='support@binance.com',
    description='Binance Internal Spread Monitoring SDK',
    url='https://github.com/binance/spread-sdk'
)
