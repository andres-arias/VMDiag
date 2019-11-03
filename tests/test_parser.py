"""
Tests for the input IP parsing routines

* Author: Andrés Arias
* Email: andres.arias12@gmail.com
"""

import pytest
from contextlib import nullcontext as does_not_raise
from vmdiag import parser


@pytest.mark.parametrize('input_list,expected', [
    (['10.10.10.1'], True),
    (['10.10.10.267'], True),
    (['10-10-10-1'], False),
    (['10-10-10-1222'], False),
    (['10.10.10.1.23.54'], False),
    (['10.10.10.1', '192.168.1.1', '192.245.0.12'], True),
    (['10.10.10.1', '192.168.1.1', '192.245.0.267'], True),
    (['10-10-10-1', '192-168-1-1', '192-245-0-12'], False),
    (['10.10.10.1222', '192.168.1.1', '192.245.0.12'], False),
    (['10.10.10.1', '192.168.1.1.56', '192.245.0.12'], False)
])
def test_format(input_list, expected):
    """
    Tests the IP format validator. Should return True on those
    IP lists where **all** the string conform to the XXX.XXX.XXX.XXX format.

    Parameters
    ----------
    input_list: list
        List containing the IP addresses to validate.
    expected: bool
        Whether the input IP addresses are **all** correct or not.
    """
    assert parser.validate_ip(input_list) == expected


@pytest.mark.parametrize('input_list,expected', [
    (['10.10.10.1'], True),
    (['10.10.10.267'], False),
    (['10.10.10.1', '192.168.1.1', '192.245.0.12'], True),
    (['10.10.10.1', '192.168.267.1', '192.245.0.267'], False)
])
def test_ip_range(input_list, expected):
    """
    Tests the IP octet range validator. Should return True on those
    IP lists where **all** the strings are formed by octets between 0-255.

    Parameters
    ----------
    input_list: list
        List containing the IP addresses to validate.
    expected: bool
        Whether the input IP addresses are **all** correct or not.
    """
    assert parser.validate_ip_octets(input_list) == expected


@pytest.mark.parametrize('input_ip,expected', [
    ('10.10.10.1', ['10.10.10.1']),
    ('10.10.10.1,192.168.1.1', ['10.10.10.1', '192.168.1.1']),
])
def test_parsing(input_ip, expected):
    """
    Tests the complete IP parser, where it gets a string containing the
    IP addresses separated by commas and return a list with the parsed
    addresses.

    Parameters
    ----------
    input_ip: string
        String containing the IP addresses separated by commas.
    expected: list
        The resulting list with the properly parsed IP addresses.
    """
    assert parser.parse_ip(input_ip) == expected


@pytest.mark.parametrize('input_ip,expected', [
    ('10.10.10.1', does_not_raise()),
    ('10.10.10.1,192.168.1.1', does_not_raise()),
    ('10.10.10.267', pytest.raises(Exception)),
    ('10.10.10.1,10.10.10.267', pytest.raises(Exception)),
    ('10-10-10-1', pytest.raises(Exception)),
    ('10-10-10-1222', pytest.raises(Exception)),
    ('10.10.10.1.23.54', pytest.raises(Exception))
])
def test_parse_except(input_ip, expected):
    """
    Tests the exception throwing on the IP parser. The parser should
    throw an exception when the format or octet range of the input IP
    addresses are wrong.

    Parameters
    ----------
    input_ip: string
        String containing the IP addresses separated by commas.
    expected: function
        Whether the input IP string should throw and exception or not.
    """
    with expected:
        assert parser.parse_ip(input_ip)


@pytest.mark.parametrize('input_ip,expected_msg', [
    ('10.10.10.267', 'Invalid IP octet. Maximum value should be 255'),
    ('10-10-10-1222', 'Invalid IP format. Should be XXX.XXX.XXX.XXX'),
    ('10.10.10.1.23.54', 'Invalid IP format. Should be XXX.XXX.XXX.XXX')
])
def test_except_messages(input_ip, expected_msg):
    """
    Tests the messages thrown by the IP parser exceptions.

    Parameters
    ----------
    input_ip: string
        String containing the IP addresses separated by commas.
    expected: string
        The messages thrown by the exception that should be raised.
    """
    with pytest.raises(Exception) as error:
        assert parser.parse_ip(input_ip)
    assert str(error.value) == expected_msg
