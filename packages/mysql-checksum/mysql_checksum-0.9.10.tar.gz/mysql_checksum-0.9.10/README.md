[![License](https://img.shields.io/github/license/demmonico/mysql-checksum)](LICENSE)
[![Pipeline](https://github.com/demmonico/mysql-checksum/actions/workflows/workflow.yml/badge.svg)](https://github.com/demmonico/mysql-checksum/actions/workflows/workflow.yml)
![GitHub Tag](https://img.shields.io/github/v/tag/demmonico/mysql-checksum)


# MySQL Checksum Package Project

## Description

MySQL Checksum is a Python script that calculates the checksum of a MySQL database. 
It can be used to verify the integrity of the database and ensure that it has not been tampered with.

It can also be used to compare the checksums of two databases to see if they are identical.

## Installation

To install the required dependencies, run the following command:

```bash
pip install mysql-checksum
```

## Usage

Run the script with the following command:

```bash
mysql-checksum <database_name> <user> <password> <host> <port>
```

## Maintenance

### Bump Version

Using [bumpversion](https://pypi.org/project/bumpversion/) to bump the version of the package.

```bash
# Install bumpversion if not already installed
pip install --upgrade bumpversion
# Bump the version
bumpversion major setup.py
```
