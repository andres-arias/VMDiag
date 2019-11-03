import paramiko
import click

class Server:
    ip_address = ''
    username = ''
    with_keys = False
    credentials = ''
    client = None
    connected = False

    def __init__(self, ip_address, username, creds, with_keys=False):
        self.ip_address = ip_address
        self.username = username
        self.client = paramiko.SSHClient()
        self.with_keys = with_keys
        if with_keys:
            self.credentials = paramiko.RSAKey.from_private_key_file(creds)
            self.client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        else:
            self.credentials = creds

    def connect(self):
        if self.with_keys:
            try:
                self.client.connect(hostname=self.ip_address,
                                    username=self.username,
                                    pkey=self.credentials,
                                    timeout=60)
                click.echo("Succesfully logged into address %s" % self.ip_address)
                self.connected = True
            except Exception as error:
                click.echo(error)
        else:
            try:
                self.client.connect(hostname=self.ip_address,
                                    username=self.username,
                                    password=self.credentials,
                                    timeout=60)
                click.echo("Succesfully logged into address %s" % self.ip_address)
                self.connected = True
            except Exception as error:
                click.echo(error)

    def desconnect(self):
        if self.connected:
            self.client.close()
