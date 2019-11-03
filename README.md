# VMDiag

Simple tool for monitoring VM CPU and memory usage

Tool developed using Python 3.7

VMDiag was developed by [Andrés Arias](https://andres-arias.github.io).


## Requirements

Besides Python 3.7, VMDiag requires the following Python packages:

* [Paramiko](http://www.paramiko.org/): For SSH access to the remote 
servers.
* [Click](https://click.palletsprojects.com): Command-line parser.


For a development environment, additional packages are required:

* [pytest](https://docs.pytest.org): For running the unit tests.
* [Sphinx](https://www.sphinx-doc.org/): For building the documentation.


## Installing

To install the package, just clone the project and run pip as shown:

```
git clone https://github.com/andres-arias/VMDiag.git
cd VMDiag
pip3 install -e .
```

### Development environment

Clone the repository:

```
git clone https://github.com/andres-arias/VMDiag.git
cd VMDiag
```

Initialize and activate a virtual environment:

```
python3 -m venv ./venv
source venv/bin/activate
```

Install the required packages:

```
pip3 install -r requirements.txt
```

#### Build the documentation

Go to the `docs` folder and run the `make` command:

```
cd docs
make html
```

The resulting documentation will be found on `docs/_build/html`


## Running tests
