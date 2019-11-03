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

    def run_cmd(self, cmd):
        stdin, stdout, stderr = self.client.exec_command(cmd)
        click.echo(stdout.read())

    def get_running_proccesses(self):
        stdin, stdout, stderr = self.client.exec_command('ps axco command --sort=-pcpu')
        process_list = []
        process_list_raw = stdout.readlines()
        process_list_raw.pop(0)
        for proc in process_list_raw:
            process_list.append(proc.rstrip())
        return process_list


    def get_top_cpu(self):
        stdin, stdout, stderr = self.client.exec_command('ps axco command,pcpu --sort=-pcpu | head -n 4')
        return self.__clean_stdout(stdout)


    def get_top_mem(self):
        stdin, stdout, stderr = self.client.exec_command('ps axco command,pmem --sort=-pmem | head -n 4')
        return self.__clean_stdout(stdout)


    def __clean_stdout(self, stdout):
        process_dict = {}
        process_list_raw = stdout.readlines()
        process_list_raw.pop(0)
        for proc in process_list_raw:
            split_list = proc.split(' ')
            clean_list = []
            for i in split_list:
                if i != '':
                    clean_list.append(i.rstrip())
            process_dict[clean_list[0]] = clean_list[1]
        return process_dict


    def get_remaining_cap(self):
        result_dict = {}
        stdin, stdout, stderr = self.client.exec_command('grep \'cpu \' /proc/stat | awk \'{usage=($2+$4)*100/($2+$4+$5)} END {print usage}\'')
        total_cpu = stdout.readlines()[0].rstrip()
        remaining_cpu = (1 - float(total_cpu)) * 100
        result_dict['cpu'] = remaining_cpu
        stdin, stdout, stderr = self.client.exec_command('cat /proc/meminfo | grep MemAvailable')
        split_list = stdout.readlines()[0].split(' ')
        clean_list = []
        for i in split_list:
            if i != '':
                clean_list.append(i.rstrip())
        result_dict['memory'] = clean_list[1] + ' ' + clean_list[2]
        return result_dict

