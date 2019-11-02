import vmdiag
import parser
import click

@click.command()
# @click.option('--count', default=1, help='Number of loops')
@click.argument('ips', nargs=-1)
def main(ips):
    ips_string = ""
    for i in ips:
        ips_string += i
    try:
        ip_list = parser.parse_ip(ips_string)
        for ip in ip_list:
            click.echo(ip)
    except Exception as error:
        click.echo(error)


if __name__ == '__main__':
    main()
