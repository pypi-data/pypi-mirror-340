from setuptools import setup, find_packages

with open("readme.md", "r") as f:
    description=f.read()
setup(
    name="WebTrader",
    version="1.0.4",
    packages=find_packages(),
    install_requiress=["pyperclip", "requests"],
    entry_points={
         "console_scripts": [
              "webtrader = WebTrader:webtrader" 
        ]
    },
    long_description=description,
    long_description_content_type="text/markdown",
    author="NecmeddinHD",
    classifiers=[
    "Programming Language :: Python :: 3",
    "License :: OSI Approved :: Apache Software License",
    "Operating System :: OS Independent",
    "Topic :: Communications :: Chat",
    "Intended Audience :: Developers",
    "Development Status :: 4 - Beta",
    "Framework :: AsyncIO",
    "Environment :: Console",
],
keywords="telegram bot share link device transfer"
)