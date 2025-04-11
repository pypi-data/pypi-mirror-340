from setuptools import setup, find_packages

with open("readme.md", "r") as f:
    description=f.read()
setup(
    name="WebTrader",
    version="1.0.3",
    packages=find_packages(),
    install_requiress=["pyperclip", "requests"],
    entry_points={
         "console_scripts": [
              "webtrader = WebTrader:webtrader" 
        ]
    },
    long_description=description,
    long_description_content_type="text/markdown"
)