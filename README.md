![Greenbone Logo](https://www.greenbone.net/wp-content/uploads/gb_logo_resilience_horizontal.png)

# Project Hyperion <!-- omit in toc -->

:warning: This project has been abandoned. Therefore this repository is unmaintained and will not get any further changes!

[![code test coverage](https://codecov.io/gh/greenbone/hyperion/branch/master/graph/badge.svg)](https://codecov.io/gh/greenbone/hyperion)
[![Build and test](https://github.com/greenbone/hyperion/actions/workflows/ci-python.yml/badge.svg)](https://github.com/greenbone/hyperion/actions/workflows/ci-python.yml)

Project Hyperion is the next generation GVM Architecture.

The project is named after the [titan Hyperion](https://en.wikipedia.org/wiki/Hyperion_(Titan)),
the titan of the light. Hyperion is the father of Helios (Sun), Selene (Moon)
and Eos (Dawn).

The project is a [django project](https://docs.djangoproject.com/en/3.0/intro/tutorial01/#creating-a-project)
consisting of the [django app](https://docs.djangoproject.com/en/3.0/ref/applications/):
Selene.

Selene is the first step of getting a whole new architecture.
  
## Table of Contents

- [Table of Contents](#table-of-contents)
- [Installation](#installation)
  - [Requirements](#requirements)
  - [Development](#development)
- [Usage](#usage)
- [Maintainer](#maintainer)
- [License](#license)

## Installation

### Requirements

Hyperion depends on django, graphene and graphene-django for selene.

Selene also requires python-gvm.

Only Python 3.7 and later is supported.

### Development

For development, you should use [poetry](https://python-poetry.org/) to keep
your Python packages separated in different environments. To manage the
environments poetry depends on the venv package.

On Debian based systems venv can be installed with

    sudo apt install python3-venv

Poetry can be installed via pip. On Debian based systems pip itself can be
installed via

    sudo apt install python3-pip

To install poetry run

    python3 -m pip install --user poetry

Afterwards run in the cloned directory of hyperion

    cd /path/to/hyperion
    poetry install

to install all dependencies including all dependencies only required for
development into a virtual python environment.

For linting and auto formatting of the Python code you should ensure that the
[autohooks](https://github.com/greenbone/autohooks) git hooks are activated.

    poetry run autohooks activate --force

## Usage

A development server can be started via

    poetry shell
    python manage.py runserver

The development server listens on localhost (127.0.0.1) and port 8000.

## Maintainer

This project is maintained by [Greenbone Networks GmbH](https://www.greenbone.net/).

## License

Copyright (C) 2019 - 2021 [Greenbone Networks GmbH](https://www.greenbone.net/)

Licensed under the [GNU Affero General Public License v3.0 or later](LICENSE).
