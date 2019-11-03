import click
import json
from vmdiag import parser, server
# import vmdiag.parser
# import vmdiag.server



@click.command()
@click.argument('ip', required=True, nargs=-1)
@click.option('--user', required=True, multiple=True, help='SSH username for the given IP addresses')
@click.option('--password', multiple=True, help='SSH password for the given IP addresses')
@click.option('--key', multiple=True, type=click.Path(), help='SSH Keys for the given IP addresses')
def main(ip, user, password, key):
    ip_string = ""
    for i in ip:
        ip_string += i
    try:
        ip_list = parser.parse_ip(ip_string)
        if len(ip_list) != len(user):
            click.echo("Error: Must provide usernames for every IP address.")
            exit()
        else:
            stats_dict = {}
            host = server.Server(ip_list[0], user[0], key[0], True, 20)
            host.connect()
            stats_dict['running_processes'] = host.get_running_proccesses()
            stats_dict['top_3_cpu_consumption'] = host.get_top_cpu()
            stats_dict['top_3_memory_consumption'] = host.get_top_mem()
            stats_dict['remaining_capacity'] = host.get_remaining_cap()
            server_json = json.dumps(stats_dict, indent=4)
            click.echo(server_json)

            with open('data.json', 'w') as f:
                json.dump(server_json, f)
    except Exception as error:
        click.echo("Error, could not connect. Reason: %s" % error)


if __name__ == '__main__':
    main()
