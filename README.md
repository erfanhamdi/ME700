# ME700-2025-MECHE-BU
[![python](https://img.shields.io/badge/python-3.12-blue.svg)](https://www.python.org/)
![os](https://img.shields.io/badge/os-ubuntu%20|%20macos%20|%20windows-blue.svg)
[![license](https://img.shields.io/badge/license-MIT-green.svg)](https://github.com/sandialabs/sibl#license)

[![codecov](https://codecov.io/gh/erfanhamdi/ME700/graph/badge.svg?token=2IUOIQ8IEM)](https://codecov.io/gh/erfanhamdi/ME700)
[![tests](https://github.com/erfanhamdi/ME700/actions/workflows/code-coverage.yml/badge.svg)](https://github.com/erfanhamdi/ME700/actions)

* This repository contains the course materials for ME700 at Boston University.

## Assignment 1
1. [Bisection Method](src/bisection_readme.md)
2. [Newton-Raphson Method](src/newton-raphson_readme.md)
3. [Elasto Plastic material](src/elasto_plastic_readme.md)

* You can find the tutorials for each assignment part in the `tutorials/` directory.

## Setup instructions
1. Create a conda environment and activate it
```
conda create --name me700-env python=3.9.13
conda activate me700-env
```
2. Install the base requirements
```
pip install --upgrade pip setuptools wheel
```
3. Install the requirements by running this command in the root directory.
```
pip install -e .
```
4. You can run the tests using the `pytest` module
```
pytest -v --cov=setupexample  --cov-report term-missing
```
