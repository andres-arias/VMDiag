"""
Connects via SSH to Linux servers to retrieve usage data:
    * Currently running processes (one interval).
    * Top 3 processes consuming CPU.
    * Top 3 processes consuming memory.
    * Remaining memory in kB and CPU percentage available.

* Author: Andrés Arias
* Email: andres.arias12@gmail.com
"""

import click
import json
from vmdiag import parser, server


def retrieve_info(ip_address, username, key):
    """
    Runs a server instance and retrieves the usage info.

    Parameters
    ----------
    ip_address: string
        IPv4 of the target server. Format: ``XXX.XXX.XXX.XXX``
    username: string
        Username to log via SSH to target server.
    key: string
        File path of the private key to log via SSH to target server.

    Returns
    -------
    dictionary
        Dictionary with the resulting usage data.
    """
    stats_dict = {}
    result_dict = {}
    client = server.Server(ip_address, username, key, 20)
    client.connect()
    stats_dict['running_processes'] = client.get_running_proccesses()
    stats_dict['top_3_cpu_consumption'] = client.get_top_cpu()
    stats_dict['top_3_memory_consumption'] = client.get_top_mem()
    stats_dict['remaining_capacity'] = client.get_remaining_cap()
    result_dict[ip_address] = stats_dict
    client.disconnect()
    return result_dict

@click.command()
@click.argument('ip', required=True, nargs=-1)
@click.option('--user', required=True, multiple=True, help='SSH username for the given IP addresses')
@click.option('--key', required=True, multiple=True, type=click.Path(), help='SSH Keys for the given IP addresses')
@click.option('--output', help='File where the output will be dumped.')
def main(ip, user, key, output):
    ip_string = ""
    for i in ip:
        ip_string += i
    try:
        ip_list = parser.parse_ip(ip_string)
        if len(user) != len(key):
            click.echo("Error: Must provide usernames and PEM keys for every IP or one PEM key common to all servers.")
            exit()
        else:
            result_dict = {}
            if len(user) == len(ip_list):
                server_count = 0
                for addr in ip_list:
                    stats_dict = retrieve_info(addr, user[server_count], key[server_count])
                    result_dict[addr] = stats_dict[addr]
                    server_count += 1
            elif len(user) == 1: # Use a common user, key pair for all servers
                for addr in ip_list:
                    stats_dict = retrieve_info(addr, user[0], key[0])
                    result_dict[addr] = stats_dict[addr]
            else:
                click.echo("Error: Must provide PEM keys and usernames for every IP or one PEM key common to all servers.")
                exit()

            server_json = json.dumps(result_dict, indent=4)
            click.echo(server_json)
            if output is None: # Gave no output file name, use default
                json_file = open('server_data.json', "w")
                json_file.write(server_json)
            else:
                json_file = open(output, "w")
                json_file.write(server_json)
            click.echo("Output stored in output file!")
            json_file.close()
    except Exception as error:
        click.echo("Error: %s" % error)


if __name__ == '__main__':
    main()
