from setuptools import setup, find_packages

setup(
    name="WebTrader",
    version="1.0.1",
    packages=find_packages(),
    install_requiress=["pyperclip", "requests"],
    entry_points={
         "console_scripts": [
              "webtrader = WebTrader.py:webtrader" 
        ]
    }
)