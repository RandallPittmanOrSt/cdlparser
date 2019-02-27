import os
from setuptools import setup

CURDIR = os.path.abspath(os.path.dirname(__file__))
version={}
exec(open(os.path.join(CURDIR, "cdlparser", "_version.py")).read(), version)

setup(
    name="cdlparser",
    version=version["__version__"],
    packages=["cdlparser"],
    install_requires=[
        'ply>=3.11,<4.0',
        'netcdf4>=1.4.2,<1.5',
        'numpy>=1.15,<1.16',
    ],
    project_urls={
        "Documentation": "https://github.com/rockdoc/cdlparser/wiki",
        "Source": "https://github.com/rockdoc/cdlparser",
        "Tracker": "https://github.com/rockdoc/cdlparser/issues",
    }
)
