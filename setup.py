from setuptools import setup, find_packages
from os import path

this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, "README.md"), encoding="utf-8") as f:
    long_description = f.read()

with open("requirements.txt", "r", encoding="utf-8") as reqs:
    install_requires = reqs.readlines()

name = "chombopy"
with open("version.txt", "r") as version_file:
    release = version_file.read().strip()
version = ".".join(release.split(".")[:-1])

test_requires = ["pytest-cov", "coverage", "pytest-html"]
setup_requires = [
    "wheel",
    "sphinx",
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
    python_requires=">=3.10",
    install_requires=install_requires
    + test_requires
    + setup_requires,
    tests_require=test_requires,
    zip_safe=False,
)
