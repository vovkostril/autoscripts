import time


class Connection:
    def __init__(self, ip, username, password):
        self.ip = ip
        self.username = username
        self.password = password
        self.connected = False
        self.logs = ""
        self.canvas_coordinates = [0,0] #x- & y-coordinates used in erps tests

    def get_ip(self):
        return self.ip

    def change_ip(self, ip):
        self.ip = ip

    def get_ip(self):
        return self.ip

    def connect(self, ssh, username=None, password=None):
        if username == None:
            username = self.username

        if password == None:
            password = self.password

        success = ssh.login(self.ip, username, password)
        if success == 0:
            self.connected = True
        else:
            self.connected = False


    def is_active(self, ssh):
        return ssh.is_active()

    def disconnect(self, ssh):
        logs = ssh.get_logs()
        self.logs = self.logs + logs
        ssh.logout()
        self.connected = False

    def is_connected(self):
        return self.connected

    def get_logs(self):
        logs = self.logs
        self.logs = ""
        return logs

    def set_sw(self, sw):
        self.sw = sw

    def get_sw(self):
        return self.sw

    def load_base_configs(self, ssh):
        self.connect(ssh)
        ssh.send("")
        dir = ssh.read_until()
        splitdir = dir.split()
        for x in splitdir:
            if x.__contains__(""):
                ssh.send("")
                time.sleep(5)
                ssh.send("")
                self.disconnect(ssh)
                return True
        self.disconnect(ssh)
        return False

    def set_coordinates(self, x, y):
        self.canvas_coordinates = [x, y]

    def get_coordinates(self):
        return self.canvas_coordinates
