from setuptools import setup, find_packages

setup(
    name="boosdklib",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        "pywebview"
    ],
    entry_points={
        "console_scripts": [
            "boosdk = boosdklib.cli:main"
        ]
    },
    author="panoscodergr",
    description="BoosSDK CLI για μετατροπή HTML σε .exe μέσω pywebview",
)
