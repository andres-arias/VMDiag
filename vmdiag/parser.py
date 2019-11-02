import re

def parse_ip(ip_string):
    ip_list = ip_string.split(',')
    if not validate_ip(ip_list):
        raise Exception('Invalid IP format. Should be XXX.XXX.XXX.XXX')
    elif not validate_ip_octets(ip_list):
        raise Exception('Invalid IP octet. Maximum value should be 255')
    else:
        return ip_list


def validate_ip(ip_list):
    for ip in ip_list:
        match_result = re.match(r'^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$', ip)
        if match_result is None:
            return False
    return True


def validate_ip_octets(ip_list):
    for ip in ip_list:
        ip_segments = ip.split('.')
        for num in ip_segments:
            if int(num) > 255 or int(num) < 0:
                return False
    return True
