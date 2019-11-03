"""
Class for connecting to remote servers via SSH and get their
consumption information.

* Author: Andrés Arias
* Email: andres.arias12@gmail.com
"""

import paramiko
import click

class Server:
    """
    Connects to a remote server via SSH. Can use password or PEM keys for
    authentication.

    Parameters
    ----------
    ip_address: string
        IPv4 address of the remote server.
    username: string
        Username to log into via SSH.
    creds: string
        Password or PEM key to use for SSH authentication. If ``with_keys`` is
        set to True, you must provide the path of the PEM file for the corresponding
        key.
    with_keys: bool
        Whether to use PEM key or password for SSH authentication.
    timeout: int
        Time in seconds to wait before giving up trying to connected.

    Attributes
    ----------
    ip_address: string
        IPv4 address of the remote server.
    username: string
        Username to log into via SSH.
    credentials: string
        Password or PEM key to use for SSH authentication.
    with_keys: bool
        Whether to use PEM key or password for SSH authentication.
    timeout: int
        Time in seconds to wait before giving up trying to connected.
    connected: bool
        Indicates if a connection is currently established or not
    """

    connected = False
    """
    bool: Indicates if a connection is currently established or not.
    """

    def __init__(self, ip_address, username, creds, with_keys=False, timeout=60):
        self.ip_address = ip_address
        self.username = username
        self.client = paramiko.SSHClient()
        self.with_keys = with_keys
        self.timeout = timeout
        if with_keys:
            self.credentials = paramiko.RSAKey.from_private_key_file(creds)
            self.client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        else:
            self.credentials = creds

    def connect(self):
        """
        Establishes a connection via SSH to the remote server using
        the parameters provided when initializing the Server object.

        Raises
        ------
        Exception
            If connection times out or server not found.
        """
        if self.with_keys:
            try:
                self.client.connect(hostname=self.ip_address,
                                    username=self.username,
                                    pkey=self.credentials,
                                    timeout=self.timeout)
                click.echo("Succesfully logged into address %s" % self.ip_address)
                self.connected = True
            except Exception as error:
                click.echo(error)
        else:
            try:
                self.client.connect(hostname=self.ip_address,
                                    username=self.username,
                                    password=self.credentials,
                                    timeout=self.timeout)
                click.echo("Succesfully logged into address %s" % self.ip_address)
                self.connected = True
            except Exception as error:
                click.echo(error)

    def desconnect(self):
        """
        Establishes a connection via SSH to the remote server using
        the parameters provided when initializing the Server object.
        """
        if self.connected:
            self.client.close()

    def get_running_proccesses(self):
        """
        Queries the server for the currently running processes (one interval) and
        returns a list with the processes names.

        Returns
        -------
        list
            A list containing strings with the name of every running processes
            on the server.

        """
        stdin, stdout, stderr = self.client.exec_command('ps axco command --sort=-pcpu')
        process_list = []
        process_list_raw = stdout.readlines()
        process_list_raw.pop(0)
        for proc in process_list_raw:
            process_list.append(proc.rstrip())
        return process_list


    def get_top_cpu(self):
        """
        Queries the server for the currently running processes (one interval) and
        returns a dictionary containing the top 3 processes consuming CPU.

        Returns
        -------
        dictionary
            A dictionary containing the top 3 processes consuming CPU, where the
            keys are de process names and the value the consumed CPU percentage.

        """
        stdin, stdout, stderr = self.client.exec_command('ps axco command,pcpu --sort=-pcpu | head -n 4')
        return self.__clean_stdout(stdout)


    def get_top_mem(self):
        """
        Queries the server for the currently running processes (one interval) and
        returns a dictionary containing the top 3 processes consuming memory.

        Returns
        -------
        dictionary
            A dictionary containing the top 3 processes consuming memory, where the
            keys are de process names and the value the consumed memory percentage.

        """
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
        """
        Queries the server for the current CPU and memory usage and returns
        the remaining CPU percentage and memory in kB available.

        Returns
        -------
        dictionary
            A dictionary where the ``cpu`` key indicates the remaining CPU
            percentage available and the ``memory_kb`` key indicates the
            remaining memory in kB.

        """
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
        result_dict['memory_kb'] = clean_list[1]
        return result_dict

