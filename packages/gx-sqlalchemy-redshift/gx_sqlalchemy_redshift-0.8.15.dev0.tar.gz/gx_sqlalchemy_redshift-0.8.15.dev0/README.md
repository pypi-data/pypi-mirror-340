# gx-sqlalchemy-redshift


This is a fork of the 
`sqlalchemy-redshift <https://github.com/sqlalchemy-redshift/sqlalchemy-redshift>`_ 
project that is installable with sqlalchemy 2 and usable with `Great Expectations <https://github.com/great-expectations/great_expectations>`_.
It is **NOT** a fully working sqlalchemy dialect. In particular, the dialect does not support the `get_columns` method.


## Local setup



```sh
python --version; # confirm python 3.10
python -m venv .venv; # create a virtual env
source .venv/bin/activate; 
pip install --upgrade pip # pip 25.0.1
pip install tox; # tox 4.25.0
tox --notest -e lint # run the linter
```

## Release
```sh
source .venv/bin/activate; 
pip install --upgrade build twine
```