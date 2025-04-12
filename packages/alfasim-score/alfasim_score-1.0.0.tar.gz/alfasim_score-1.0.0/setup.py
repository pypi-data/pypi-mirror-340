from setuptools import find_packages
from setuptools import setup

with open("README.rst", encoding="UTF-8") as readme_file:
    readme = readme_file.read()

with open("CHANGELOG.rst", encoding="UTF-8") as changelog_file:
    history = changelog_file.read()

requirements = [
    "alfasim-sdk==1.0.0",
    "attrs>=18.1.0",
    "numpy>=1.11.0",
    "pandas>=2.0.0",
    "oop-ext>=1.1",
    "typing_extensions",
]
extras_require = {
    "testing": [
        "codecov",
        "mypy",
        "pre-commit",
        "pytest",
        "pytest-cov",
        "pytest-mock",
        "pytest-regressions",
        "tox",
    ],
}

setup(
    author="ESSS",
    author_email="foss@esss.co",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
    ],
    description="Python package to convert the SCORE input JSON to Alfacase",
    extras_require=extras_require,
    install_requires=requirements,
    license="MIT license",
    long_description=readme + "\n\n" + history,
    include_package_data=True,
    python_requires=">=3.8",
    keywords="ALFAsim,Score",
    name="alfasim-score",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    url="https://github.com/ESSS/alfasim-score",
    zip_safe=False,
)
