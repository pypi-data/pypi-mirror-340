from setuptools import setup, find_packages
from pathlib import Path

this_directory = Path(__file__).resolve().parent
long_description = (this_directory / "README.md").read_text(encoding="utf-8")

setup(
    name="matrixx",
    version="0.1.0",
    author="Kranthi",
    author_email="kdevprofile@gmail.com",
    description="A lightweight matrix utility library",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/devk-op/matrix-utils",
    license="MIT",
    packages=find_packages(),
    include_package_data=True,
    install_requires=["numpy"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    keywords=["matrix", "linear algebra", "numerical", "utils"],
    python_requires=">=3.6",
)
