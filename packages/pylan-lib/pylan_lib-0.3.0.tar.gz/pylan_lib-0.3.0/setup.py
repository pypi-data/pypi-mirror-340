"""Python setup.py for pylan package"""

import io
import os

from setuptools import find_packages, setup


def read(*paths, **kwargs):
    content = ""
    with io.open(
        os.path.join(os.path.dirname(__file__), *paths),
        encoding=kwargs.get("encoding", "utf8"),
    ) as open_file:
        content = open_file.read().strip()
    return content


def read_requirements(path: str) -> list:
    return [
        line.strip()
        for line in read(path).split("\n")
        if not line.startswith(('"', "#", "-", "git+"))
    ]


setup(
    name="pylan-lib",
    version=os.environ["VERSION"],
    description="Python library that simulates the combined impact of recurring events.",
    url="https://github.com/TimoKats/pylan",
    long_description=read("misc/docs.md"),
    long_description_content_type="text/markdown",
    author="Timo Kats",
    author_email="hello@timokats.xyz",
    license="BSD",
    packages=find_packages(exclude=[".github"]),
    install_requires=read_requirements("requirements.txt"),
    keywords=["timeseries", "simulation", "planning"],
)
