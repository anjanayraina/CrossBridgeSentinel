# setup.py
from setuptools import setup, find_packages

setup(
    name="crossbridge-sentinel",
    version="0.1.0",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[
        "fastapi>=0.95",
        "uvicorn[standard]>=0.23",
        "pydantic>=2.0",
        "python-dotenv>=1.0",
        "web3>=6.0",
        "solana>=0.27",
        "redis>=4.5",
    ],
)
