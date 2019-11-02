"""
Functions for parsing and validating the provided IP addresses.

* Author: Andrés Arias
* Email: andres.arias12@gmail.com

Notes
-----
    ``validate_ip()`` and ``validate_ip_octets()`` are auxiliary functions, they
    are called when ``parse_ip()`` is called. If any of those auxiliary functions
    fail, ``parse_ip()`` will raise and exception.
"""

import re

def parse_ip(ip_string):
    """
    Returns a list with properly formatted IP addresses from a single
    IP address returned by Click.

    Notes
    -----
        * The function will raise an exception if the given string is ill-formed, has
          addresses with an erroneous format (*not XXX.XXX.XXX.XXX*) or if the IP address
          has an octet with a value greater than 255.

    Parameters
    ----------
    ip_string : string
        String containing the received IP addresses. The given IP string should
        follow the format: ``XXX.XXX.XXX.XXX,XXX.XXX.XXX.XXX,...``

    Returns
    -------
    list
        A list containing every received IP address as a string.

    Raises
    ------
    Exception
        Invalid IP format. Should be XXX.XXX.XXX.XXX
    Exception
        Invalid IP octet. Maximum value should be 255
    """
    ip_list = ip_string.split(',')
    if not validate_ip(ip_list):
        raise Exception('Invalid IP format. Should be XXX.XXX.XXX.XXX')
    elif not validate_ip_octets(ip_list):
        raise Exception('Invalid IP octet. Maximum value should be 255')
    else:
        return ip_list


def validate_ip(ip_list):
    """
    Validates that every given IP address conforms with the format
    XXX.XXX.XXX.XXX

    Parameters
    ----------
    ip_list : list
        List containing the received IP addresses.

    Returns
    -------
    bool
        A boolean indicated whether every provided IP address follows the
        correct format or not.
    """
    for ip in ip_list:
        match_result = re.match(r'^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$', ip)
        if match_result is None:
            return False
    return True


def validate_ip_octets(ip_list):
    """
    Validates that every octet in the given IP list is between the 0-255 range.

    Parameters
    ----------
    ip_list : list
        List containing the received IP addresses.

    Returns
    -------
    bool
        A boolean indicated whether every provided IP address is between the
        correct range or not.

    """
    for ip in ip_list:
        ip_segments = ip.split('.')
        for num in ip_segments:
            if int(num) > 255 or int(num) < 0:
                return False
    return True
