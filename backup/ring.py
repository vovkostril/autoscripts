from itertools import filterfalse
import ip
import time
import ssh_connector
import datetime
import serial
import threading



class ITU_T_G_8032:
    ROBOT_LIBRARY_SCOPE = 'GLOBAL'


    def __init__(self):
        self.ssh = ssh_connector.SSHConnection()
        self.ce_list = []
        self.ip1 = ip.Connection("", "admin", "")
        self.ip2 = ip.Connection("", "admin", "")
        self.ip3 = ip.Connection("", "admin", "")
        # next ip addresses 
        self.ce_list.append(self.ip1)
        # 
        self.ip_list = []
        self.serial = None
        self.serial2 = None
        self.read = False

    def get_logs(self):
        logs_list = []
        for ce in self.ce_list:
            logs_list.append(ce.get_logs())
        return logs_list

    def wait_and_connect(self, ce):
        time.sleep(1)
        timeout = datetime.datetime.now() + datetime.timedelta(minutes=5)
        while datetime.datetime.now() < timeout:
            try:
                ce.connect(self.ssh)
            except:
                time.sleep(20)
            if ce.is_connected():
                break
        if not ce.is_connected():
            raise Exception("No connection.")
    def tp(self):
        for ce in self.ce_list:
            ce.connect(self.ssh)
            print(self.ssh.send_and_read(""))

    def open_serials(self):
        try:
            self.serial = serial.Serial("/dev/serial/by-id/usb-FTDI_FT232R_USB_UART_AD0K0OE8-if00-port0", 115200, timeout=5)
            self.serial2 = serial.Serial("/dev/serial/by-id/usb-FTDI_FT232R_USB_UART_AI05F39F-if00-port0", 115200, timeout=5)
            self.read = True
            self.t = threading.Thread(target=self.serial_read, daemon=True)
            self.t.start()
            return "serial connection found"
        except:
            return "no serial connection"

    def serial_read(self):
        f = open("consoleone.txt", "w+")
        f.truncate(0)
        f.close()
        f = open("consoletwo.txt", "w+")
        f.truncate(0)
        f.close()
        c1 = open("consoleone.txt", "a")
        c2 = open("consoletwo.txt", "a")
        while self.read == True:
            line = self.serial.readline()
            s1 = str(line, "utf-8")
            c1.write(s1)
            line = self.serial2.readline()
            s2 = str(line, "utf-8")
            c2.write(s2)
        c1.close()
        c2.close()
        self.serial.close()
        self.serial2.close()

    def close_serials(self):
        # time.sleep(300)
        self.read = False
        time.sleep(10)
        return "Done"

    def configure(self):
        for ce in self.ce_list:
            neighbours = []
            ports = []

            #Get neighbour ip-addresses
            ce.connect(self.ssh)
            managements = self.ssh.send_and_read("")
            print(managements)
            managements = managements.split()
            for y in managements:
                if y.__contains__("192.168."):
                    neighbours.append(y)

            #Get ports where neighbours are connected
            description = self.ssh.send_and_read("")
            print(description)
            description = description.split()
            for y in range(0, len(description)):
                p = description[y]
                if p.__contains__(""):
                    ports.append(description[y]+" "+description[y+1])

            #
            print("")
            print(neighbours)
            print(ports)
            #
            print(len(neighbours))
            print(len(ports))
            remove = []
            for ce_i in neighbours:
                if ce_i not in self.ip_list:
                    remove.append(ce_i)
            for ce_i in remove:
                i = neighbours.index(ce_i)
                neighbours.remove(ce_i)
                # ports.pop(i)
            # print("Before removing:")
            # print(ports)
            # for port in ports:
                # print("Check ports: "+port)
                # if not '' in port:
                # i = ports.index(ports)
                    # ports.remove(port)
            ports = [port for port in ports if '' in port]
            print("There are neighbours: ")
            print(neighbours)
            print(ports)
            print("s")
            print(len(neighbours))
            print(len(ports))
            for x in range(len(ports)):
                print(ports[1])

            for x in range(len(ports)):

                ip = ce.get_ip()
                s = ip.split(".")
                mepid = s[3]
                mepid = mepid[-2:]

                neighbour = neighbours[x]
                s = neighbour.split(".")
                peer_mepid = s[3]
                peer_mepid = peer_mepid[-2:]
                time.sleep(20)

                self.ssh.send("configure terminal")
                self.ssh.send("")
                self.ssh.send("")
                self.ssh.send("end")

                mep = self.ssh.send_and_read("show")
                print(mep)
            ce.disconnect(self.ssh)

        #
        o = self.ip1
        n = self.ip2

        o.connect(self.ssh)
        self.ssh.send("configure terminal")
        self.ssh.send("")
        self.ssh.send("")
        o.disconnect(self.ssh)

        n.connect(self.ssh)
        self.ssh.send("configure terminal")
        self.ssh.send("")
        self.ssh.send("end")
        n.disconnect(self.ssh)
        return "Done"

    def test_one(self):
        # TEST 1 
        passed = 0
        total = len(self.ce_list)
        for x in self.ce_list:
            x.connect(self.ssh)
            for _ in range(15):
                erps = self.ssh.send_and_read("show")
                #erps = ssh.read_until()
                if erps.__contains__("IDLE"):
                    print("IDLE") # POISTA
                    passed += 1
                    break
                else:
                    print(erps) # POISTA
                    x.disconnect(self.ssh)
                    for y in self.ce_list:
                        y.connect(self.ssh)
                        
                        
                        y.disconnect(self.ssh)
                    x.connect(self.ssh)
                    time.sleep(20)
            x.disconnect(self.ssh)

        if passed == total:
           return "Passed"
        else:
            return "Failed"

    def test_two(self):
        # TEST 2
        test_prot = 0
        test_pend = 0
        test_idle = 0
        owner = self.ip1
        neighbour = self.ip2
        owner.connect(self.ssh)
        ip_list = []
        for ce in self.ce_list:
            ip = ce.get_ip()
            ip_list.append(ip)
        ports = []
        nei_ips = []

        #
        description = self.ssh.send_and_read("")
        description = description.split()
        for y in range(0, len(description)):
            p = description[y]
            if p.__contains__(""):
                ports.append(description[y]+" "+description[y+1])

        description = self.ssh.send_and_read("")
        description = description.split()
        for y in range(0, len(description)):
            p = description[y]
            if p.__contains__(""):
                nei_ips.append(description[y])

        shutdown_port = None
        for n in range(len(nei_ips)):
            ip = nei_ips[n]
            if ip in ip_list and ip != neighbour.get_ip():
                shutdown_port = ports[n]

        self.ssh.send("configure terminal")
        self.ssh.send(""+shutdown_port)
        self.ssh.send("")
        self.ssh.send("")

        time.sleep(1)
        erps = self.ssh.send_and_read("")
        if erps.__contains__("PROT"):
            test_prot += 1

            self.ssh.send("con t")
            self.ssh.send(" "+ shutdown_port)
            self.ssh.send("")
            self.ssh.send("end")

            time.sleep(1)
            for _ in range(5):
                erps = self.ssh.send_and_read("")
                if erps.__contains__("PEND"):
                    test_pend += 1
                    break
                else:
                    self.ssh.send("")
                    self.ssh.send("")
                    time.sleep(15)

            time.sleep(1)
            for _ in range(5):
                erps = self.ssh.send_and_read("")
                if erps.__contains__("IDLE"):
                    test_idle += 1
                    break
                else:
                    self.ssh.send("")
                    self.ssh.send("")
                    time.sleep(15)

            owner.disconnect(self.ssh)

        if test_prot == 1 and test_pend == 1 and test_idle == 1:
            return "Passed"
        else:
            return "Failed"

    def test_three(self):
        #Test 3
        test_prot = 0
        test_pend = 0
        test_idle = 0
        owner = self.ip1
        reload_ce = self.ip2

        reload_ce.connect(self.ssh)
        self.ssh.send("")
        time.sleep(20)
        self.ssh.send("")
        reload_ce.disconnect(self.ssh)
        time.sleep(50)
        owner.connect(self.ssh)

        for _ in range(5):
            erps = self.ssh.send_and_read("")
            #erps = ssh.read_until()
            if erps.__contains__("PROT"):
                test_prot += 1
                break
            else:
                time.sleep(10)

        for _ in range(10):
            erps = self.ssh.send_and_read("")
            #erps = ssh.read_until()
            if erps.__contains__("PEND"):
                test_pend += 1
                break
            else:
                time.sleep(10)

        for _ in range(10):
            erps = self.ssh.send_and_read("")
            #erps = ssh.read_until()
            if erps.__contains__("IDLE"):
                test_idle += 1
                break
            else:
                time.sleep(10)

        owner.disconnect(self.ssh)
        if test_prot == 1 and test_pend == 1 and test_idle == 1:
            return "Passed"
        else:
            return "Failed"


    def cleanup(self):

        for ce in self.ce_list:
            ce.connect(self.ssh)
            ports = []
            #Get ports where neighbours are connected
            description = self.ssh.send_and_read("")
            description = description.split()
            for y in range(0, len(description)):
                p = description[y]
                if p.__contains__(""):
                    ports.append(description[y]+" "+description[y+1])

            for y in ports:
                self.ssh.send("configure termina")
                self.ssh.send("end")
            ce.disconnect(self.ssh)
        return "Done"

    def make_backups(self):
        for ce in self.ce_list:
            ce.connect(self.ssh)
            self.ssh.send("")
            time.sleep(12)
            ce.disconnect(self.ssh)
        time.sleep(10)
        self.ce120.connect(self.ssh)
        flash = self.ssh.send_and_read("")
        self.ce120.disconnect(self.ssh)
        return flash

    def load_backups(self):
        for ce in self.ce_list:
            ce.connect(self.ssh)
            self.ssh.send("")
            time.sleep(10)
            self.ssh.send("")
            time.sleep(2)
            self.ssh.send("")
            ce.disconnect(self.ssh)

        for ce in self.ce_list:
            self.wait_and_connect(ce)
            flash = self.ssh.send_and_read("")
            ce.disconnect(self.ssh)
            time.sleep(30)
            return flash




