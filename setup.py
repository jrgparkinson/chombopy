from setuptools import setup, find_packages
from os import path

this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, "README.md"), encoding="utf-8") as f:
    long_description = f.read()

name = "chombopy"
version = "0.2"
release = "0.2.1"

test_requires = ["pytest-cov", "coverage", "pytest-html"]
setup_requires = [
    "wheel==0.34.2",
    "sphinx==2.4.4",
    "docutils==0.16",
    "recommonmark==0.6.0",
    "cython<0.30",
    "numpy==1.18.5",
    "numpydoc==1.1.0"
]

setup(
    name=name,
    version=release,
    description="Running, analysing and plotting Chombo simulations",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/jrgparkinson/chombopy",
    author="Jamie Parkinson",
    author_email="jamie.parkinson@gmail.com",
    license="MIT",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    setup_requires=setup_requires,
    python_requires=">=3.6",
    install_requires=[
        "matplotlib==3.0.0",
        "Shapely>=1.6.0",
        "geopandas==0.6.2",
        "scipy==1.1.0",
        "xarray>=0.11.3",
        "h5py>=2.9.0",
        "descartes",
        "pyproj<=1.9.6",
        "pandas==1.1"
    ]
    + test_requires
    + setup_requires,
    tests_require=test_requires,
    zip_safe=False,
)
