# VMDiag

Simple tool for monitoring VM CPU and memory usage.

`vmdiag` can connect to any remove server using SSH and will report the following
statistics:

* Currently running processes (one interval).
* Top 3 processes consuming CPU.
* Top 3 processes consuming memory.
* Remaining memory in kB and CPU percentage available.

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

## Usage

```
Usage: vmdiag [OPTIONS] IP...

Options:
  --user TEXT    SSH username for the given IP addresses  [required]
  --key PATH     SSH Keys for the given IP addresses  [required]
  --output TEXT  File where the output will be dumped.
  --help         Show this message and exit.
```

`vmdiag` receives the following parameters:

* IP addresses of the remote servers, comma separated: `XXX.XXX.XXX.XXX, YYY.YYY.YYY.YYY, ...`
* Usernames for SSH connections: `--user user1 --user user1`
* You can also provide one single username to be used by all servers: `--user username`
* Path to the PEM keys used for authenticating: `--key PATH1 --key PATH2`
* As with the usernames, you can also provide one single key to be used by all
servers: `--key PATH`
* (OPTIONAL) a file path to store the output of the tool. If not given, a default
value of `./server_data.json` will be used


### Example commands:
```
vmdiag 54.200.130.35 --user ubuntu --key ~/Downloads/TestDevKey.pem
vmdiag 54.191.214.144,35.166.60.105,54.200.130.35 --user ubuntu --key ~/Downloads/TestDevKey.pem
vmdiag 54.191.214.144,35.166.60.105,54.200.130.35 --user ubuntu --key ~/Downloads/TestDevKey.pem --output data.json
vmdiag 54.191.214.144,35.166.60.105 --user ubuntu --user debian --key ~/Downloads/TestDevKey.pem --key ~/Downloads/TestDevKey.pem --output data.json
```

### Output

`vmdiag` will output the resulting statistics as JSON;

```
{
    "XXX.XXX.XXX.XXX": {
        "running_processes": [
            ...
        ],
        "top_3_cpu_consumption": {
            "proc1": 0.3,
            "proc2": 0.2,
            "proc3": 0.1
        },
        "top_3_memory_consumption": {
            "proc1": 2.4,
            "proc2": 2.0,
            "proc3": 1.9
        },
        "remaining_capacity": {
            "cpu": 84.3839,
            "memory_kb": 729240
        }
    },
    ...
}
```

The resulting JSON will be shown on the console and will be stored on a file provided by the 
`--output` option (if no output provided, it will be stored by default on `./server_data.json`).

## Running tests

* In order to run tests, three testing VM are currently instantiated on AWS EC2. The testing
machines require a private key to accept remote connections, including the ones 
performed by `vmdiag`. **The private key should be personally provided by
[me](https://github.com/andres-arias)**.

* Once you have the private key, you have to move it into the `certs` directory on project's root:

* The private key file should be named `TestDevKey.pem` and located on the path
`VMDIAG_PATH/certs/TestDevKey.pem`


Once the private key is properly setup, you can easily run the tests on the project
root directory by running the command:
```
python -m pytest -v # For verbose output
python -m pytest    # For quiet output
```

