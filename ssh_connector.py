import paramiko
import time
import logging
import os
import subprocess

def ping(hostname="127.0.0.1"):
    """
    Ping is needed before login can be attempted, because of switch over
    :return: if successful 0
    """
    proc = subprocess.Popen(['ping','-c','1', hostname],stdout=subprocess.PIPE)
    stdout, stderr = proc.communicate()
    if str(stdout).__contains__("Destination Host Unreachable") or str(stdout).__contains__("Request timed out"):
        response = 1
    elif str(stdout).__contains__("1 received"):
        response = 0
    else:
        response = 1

    return response

class SSHConnection:
    def __init__(self):
        self.client = paramiko.SSHClient()
        self.client.set_missing_host_key_policy(paramiko.AutoAddPolicy)
        self.timeout = 50.0
        path = os.path.dirname(__file__)
        self.logs = ""

    def get_logs(self):
        logs = self.logs
        self.logs = ""
        return logs

    def login(self, hostname="127.0.0.1", username="admin", password=""):
        """
        Test connectivity
        Login
        Return login text
        :param hostname:
        :param username:
        :param password:
        :return: if successful 0
        """
        connection = ping(hostname)
        if connection == 0:
            try:
                self.client.connect(hostname=hostname, port=22, username=username, password=password, timeout=25.0, allow_agent=False, look_for_keys=False, banner_timeout=2)
            except:
                time.sleep(45)
                self.client.connect(hostname=hostname, port=22, username=username, password=password, timeout=25.0, allow_agent=False, look_for_keys=False, banner_timeout=2)
            self.shell = self.client.invoke_shell()
            self.empty()
        else:
            print("connection down")
        return connection

    def logout(self):
        """
        Logout of the node by closing the connection
        :return: None
        """
        self.client.close()

    def send(self, cmd):
        """
        Send string to the shell
        :return: None
        """
        # Add new line to command string and send it to node
        cmd += "\n"
        self.shell.send(cmd)
        time.sleep(1)  # Prevent sending commands too fast for the device
        self.read_until()

    def send_and_read(self, cmd, wait=0.5):
        """
        Send string to the shell
        :return: Output in shell
        """
        # Add new line to command string and send it to node
        cmd += "\n"
        # print("I'm in.")
        self.shell.send(cmd)
        time.sleep(wait)  # Prevent sending commands too fast for the device
        output = self.read_until()
        return output

    def read_until(self, prompt="#", log=True):
        # print everything in buffer until prompt is found
        # in error case print everything found so far
        output = ""
        # print("Here start or read untill.")
        time.sleep(2)
        start = time.time()
        while time.time() - start < self.timeout:
            a = self.shell.recv(9999)
            # print("Shell invoked!")
            output += a.decode()
            print(output)
            if "-- more --, next page:" in output:
                # print("Catched!!!")
                self.shell.send("g\n")
            if output.find(prompt) > -1:
                # print("Here is end of promt!")
                self.logs = self.logs + output
                # print("End of output")
                # print("Here?")
                # print(self.logs)
                return output
        # Prompt not found in time
        #logger.log("read_until: {}".format(output))
        # Should raise exception
        #raise Exception("Timeout from reading output")

    def empty(self):
        self.send(" ")
