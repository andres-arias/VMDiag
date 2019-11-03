"""
Tests for the SSH client module.

* Author: Andrés Arias
* Email: andres.arias12@gmail.com
"""

import pytest
from vmdiag import server
from contextlib import nullcontext as does_not_raise
from os import path


@pytest.fixture
def provide_client():
    """
    Establishes a connection with the testing VM
    Returns
    -------
    Server
        Server instance already connected to the test VM
    """
    client = server.Server('54.191.214.144',
                         'ubuntu',
                         './certs/TestDevKey.pem',
                         10)
    client.connect()
    return client


@pytest.mark.parametrize('input_parameters,expected', [
    (['54.191.214.144', 'ubuntu', './certs/TestDevKey.pem'], does_not_raise()),
    (['10.10.10.1', 'ubuntu', './certs/TestDevKey.pem'], pytest.raises(Exception)),
    (['54.191.214.145', 'ubuntu', './certs/TestDevKey.pem'], pytest.raises(Exception)),
    (['54.191.214.144', 'badname', './certs/TestDevKey.pem'], pytest.raises(Exception)),
    (['54.191.214.144', 'ubuntu', './certs/badcert.pem'], pytest.raises(Exception)),
])
def test_connection_keys(input_parameters, expected):
    """
    Tests the SSH connection routines and checks whether the connection was
    successful or not

    Parameters
    ----------
    input_parameters list
        List containing the IP, username and PEM key for the server.
    expected: bool
        Whether the connection attempt should raise an exception or not.
    """
    with expected:
        client = server.Server(input_parameters[0],
                             input_parameters[1],
                             input_parameters[2],
                             10)
        assert client.connect() is None
        assert client.disconnect() is None


def test_running_processes(provide_client):
    """
    Tests if the SSH client can successfully retrieve a list of
    running processes on the remote server.
    """
    client = provide_client
    process_list = client.get_running_proccesses()
    assert len(process_list) > 0 # Process list should always contain something
    for proc in process_list:
        assert len(proc) > 0 # Every process should have a name
    client.disconnect()


def test_top_cpu(provide_client):
    """
    Tests if the SSH client can retrieve a list of the top 3 CPU consuming processes
    and checks if the resulting dictionary is ordered from greater to lower.
    """
    client = provide_client
    cpu_dict = client.get_top_cpu()
    assert len(cpu_dict) == 3 # Should always return 3 elements
    proc_count = 0
    for proc in cpu_dict:
        assert isinstance(cpu_dict[proc], float) # CPU values should be floats
        # CPU values should be between 0 and 100
        assert cpu_dict[proc] >= 0.0
        assert cpu_dict[proc] <= 100.0
        # CPU values should come from greater to lower:
        if proc_count != 0:
            assert cpu_dict[proc] <= last_proc
        last_proc = cpu_dict[proc]
        proc_count += 1
    client.disconnect()


def test_top_memory(provide_client):
    """
    Tests if the SSH client can retrieve a list of the top 3 memory consuming processes
    and checks if the resulting dictionary is ordered from greater to lower.
    """
    client = provide_client
    mem_dict = client.get_top_mem()
    assert len(mem_dict) == 3 # Should always return 3 elements
    proc_count = 0
    for proc in mem_dict:
        assert isinstance(mem_dict[proc], float) # Memory values should be floats
        # Memory values should be between 0 and 100
        assert mem_dict[proc] >= 0.0
        assert mem_dict[proc] <= 100.0
        # Memory values should come from greater to lower:
        if proc_count != 0:
            assert mem_dict[proc] <= last_proc
        last_proc = mem_dict[proc]
        proc_count += 1
    client.disconnect()


def test_remaining_capacity(provide_client):
    """
    Tests if the SSH client can retrieve the remaining CPU and memory available
    Checks if the retrieved values are between the acceptable range.
    """
    client = provide_client
    capacity_dict = client.get_remaining_cap()
    assert isinstance(capacity_dict['cpu'], float)
    assert isinstance(capacity_dict['memory_kb'], int)
    assert capacity_dict['cpu'] >= 0.0
    assert capacity_dict['cpu'] <= 100.0
    assert capacity_dict['memory_kb'] >= 0.0
    client.disconnect()
