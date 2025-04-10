from setuptools import setup, find_packages
import codecs
import os
import pathlib
HERE = pathlib.Path(__file__).parent
README = (HERE / "README.md").read_text()

VERSION = '0.0.732' 
DESCRIPTION = 'This is used for analyzing the obtain from IoT AirQo devices'
LONG_DESCRIPTION = README 

# Setting up
setup(
    name="airqloudanalysis",
    version=VERSION,
    author="AirQo",
    author_email="<gibson@airqo.net>",
    description=DESCRIPTION,
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/OlukaGibson/deviceAnalysisLibrary.git",
    packages=find_packages(),
    install_requires=['numpy', 'pandas', 'requests', 'pytz', 'python-dateutil', 'beautifulsoup4', 'matplotlib', 'seaborn', 'plotly', 'cufflinks'],
    keywords=['python', 'IoT', 'AirQo', 'data', 'analysis', 'insights'],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
        "Operating System :: POSIX :: Linux",
    ]
)