import os, sys
import serial
from serial import SerialException
import datetime, time


class Gps_time():
    def __init__(self):
        self.set_date = ""
        self.set_time = ""
    def get_time(self):
        try:
            self.gps = serial.Serial('/tty/USB0', 4800, timeout=1)
        except:
            return "ERROR"    
        while(1):
            response = self.gps.readline().decode('ascii')     							# read up to return data 30 bytes (timeout)
#            print(response)
            if (response.split(',')[0] == "$GPRMC"):
                date = datetime.datetime.strptime(response.split(',')[9], '%d%m%y')
#                print("DATE : ", date.year, date.month, date.day)
                self.set_date = str(date.year) + "-" + str(date.month) + "-" + str(date.day)
#                print(set_date)
            if (response.split(',')[0] == "$GPGGA"):
                now = datetime.datetime.strptime(response.split(',')[1].split('.')[0], '%I%M%S')
#                print("Now", now.hour+ 8, now.minute, now.second)
                self.set_time = str(now.hour+ 8) + ":" + str(now.minute) + ":" + str(now.second)
#                print(set_time)
            if (self.set_time != "" and self.set_date != ""):
#               print("set GPS time")
                command = 'sudo date -s "' + self.set_date + ' ' + self.set_time + '"'
                os.system(command)
                break
        self.gps.close()
        return "OK"

class File_search():
    def __init__(self):
        pass

    def ini_list(self):
        self.ini_table = os.listdir('/home/pi/ini/')
        return  self.ini_table

class Time_config():
    def __init__(self):
        pass

    def date_set(self, year, month, date):
        now = datetime.datetime.now()
        self.date_command = 'sudo date -s "' + year + '-' + month + '-' + date + " " + str(now.hour) + ':' + str(now.minute) + ':' + str(now.second) + '"'
#        print(self.date_command)
        os.system(self.date_command)
    
    def time_set(self, hour, minute, second):
        now = datetime.datetime.now()
        self.time_command = 'sudo date -s "' + str(now.year) + '-' + str(now.month) + '-' + str(now.day) + " " + hour + ':' + minute + ':' + second + '"'
#        print(self.time_command)
        os.system(self.time_command)

class Ntp_config():
    def __init__(self):
#       need install ntpdate By 'sudo apt-get install ntpdate'
        os.system('timedatectl set-timezone "Asia/Taipei"')
        os.system('sudo /etc/init.d/ntp stop >/tmp/ntp_stop.log')
        try:
            f = open('/etc/network/ntp.log', 'r')
            f.close()
        except:
            os.system('cp ./library/ntp.log /etc/network/ntp.log')

    def ntp_set(self, ntp_host):
        self.ntp_command = 'sudo ntpdate ' + ntp_host
        self.f = open('/etc/network/ntp.log', 'w')
        self.f.write(ntp_host)
        self.f.close()
        os.system(self.ntp_command)

class Net_config():
    def __init__(self):
        try:
            f = open('/etc/network/interfaces.bak')
            f.close()
        except:
            os.system('sudo cp ./library/interfaces.bak /etc/network/interfaces')
        try:
            f = open('/etc/network/Restusb.py')
            f.close()
        except:
            os.system('sudo cp ./library/Restusb.py /etc/network/Restusb.py')

    def eth0_dhcp(self):
        os.system("sudo sed -i '3c iface eth0 inet dhcp' /etc/network/interfaces")
        os.system("sudo sed -i '4c \\ ' /etc/network/interfaces")
        os.system("sudo sed -i '5c \\ ' /etc/network/interfaces")
        os.system("sudo sed -i '6c \\ ' /etc/network/interfaces")
        os.system('sudo ifdown eth0')
        os.system('sudo ifup eth0')
        os.system('sudo cp /etc/network/interfaces ./library/interfaces.bak')

    def eth1_dhcp(self):
        os.system("sudo sed -i '12c iface eth1 inet dhcp' /etc/network/interfaces")
        os.system("sudo sed -i '13c \\ ' /etc/network/interfaces")
        os.system("sudo sed -i '14c \\ ' /etc/network/interfaces")
        os.system("sudo sed -i '15c \\ ' /etc/network/interfaces")
        os.system('lsusb | grep "Realtek" | cut -c16,17,18 >/tmp/usb.txt')
        self.usb_id = open('/tmp/usb.txt')
        self.usb_reset = 'sudo python /etc/network/Restusb.py -d ' + self.usb_id.read()
        os.system(self.usb_reset)
        os.system('sudo cp /etc/network/interfaces /etc/network/interfaces.bak')

    def eth0_static(self, ip, netmask, gateway):
        os.system("sudo sed -i '3c iface eth0 inet static' /etc/network/interfaces")
        command = "sudo sed -i '4c address " + ip + "' /etc/network/interfaces"
        os.system(command)
        command = "sudo sed -i '5c netmask " + netmask + "' /etc/network/interfaces"
        os.system(command)
        command = "sudo sed -i '6c gateway " + gateway + "' /etc/network/interfaces"
        os.system(command)
        os.system('sudo ifdown eth0')
        os.system('sudo ifup eth0')
        os.system('sudo cp /etc/network/interfaces /etc/network/interfaces.bak')

    def eth1_static(self, ip, netmask, gateway):
        self.f = open('/etc/network/interfaces', 'r+')
        self.f.seek(190)
        self.f.write('allow-hotplug eth1\n\n')
        os.system("sudo sed -i '12c iface eth1 inet static' /etc/network/interfaces")
        command = "sudo sed -i '13c address " + ip + "' /etc/network/interfaces"
        os.system(command)
        command = "sudo sed -i '14c netmask " + netmask + "' /etc/network/interfaces"
        os.system(command)
        command = "sudo sed -i '15c gateway " + gateway + "' /etc/network/interfaces"
        os.system(command)
        os.system('lsusb | grep "Realtek" | cut -c16,17,18 >/tmp/usb.txt')
        self.usb_id = open('/tmp/usb.txt')
        self.usb_reset = 'sudo python /etc/network/Restusb.py -d ' + self.usb_id.read()
        os.system(self.usb_reset)
        os.system('sudo cp /etc/network/interfaces /etc/network/interfaces.bak')

    def eth0_dns(self, dns):
        command = "sudo sed -i '7c dns-nameserver " + dns + "' /etc/network/interfaces"
        os.system(command)
        os.system("sudo sed -i '8c \\ ' /etc/network/interfaces")
        os.system('sudo ifdown eth0')
        os.system('sudo ifup eth0')
        os.system('sudo cp /etc/network/interfaces /etc/network/interfaces.bak')

    def eth1_dns(self, dns):
        command = "sudo sed -i '16c dns-nameserver " + dns + "' /etc/network/interfaces"
        os.system(command)
        os.system("sudo sed -i '17c \\ ' /etc/network/interfaces")
        os.system('lsusb | grep "Realtek" | cut -c16,17,18 >/tmp/usb.txt')
        self.usb_id = open('/tmp/usb.txt')
        self.usb_reset = 'sudo python /etc/network/Restusb.py -d ' + self.usb_id.read()
        os.system(self.usb_reset)
    
    def eth0_dual_dns(self, dns, sub_dns):
        command = "sudo sed -i '7c dns-nameserver " + dns + "' /etc/network/interfaces"
        os.system(command)
        command = "sudo sed -i '8c dns-nameserver " + sub_dns + "' /etc/network/interfaces"
        os.system(command)
        os.system('sudo ifdown eth0')
        os.system('sudo ifup eth0')
    
    def eth1_dual_dns(self, dns, sub_dns):
        command = "sudo sed -i '16c dns-nameserver " + dns + "' /etc/network/interfaces"
        os.system(command)
        command = "sudo sed -i '17c dns-nameserver " + sub_dns + "' /etc/network/interfaces"
        os.system(command)
        os.system('lsusb | grep "Realtek" | cut -c16,17,18 >/tmp/usb.txt')
        self.usb_id = open('/tmp/usb.txt')
        self.usb_reset = 'sudo python /etc/network/Restusb.py -d ' + self.usb_id.read()

    def eth0_auto_dns(self):
        command = "sudo sed -i '7c dns-nameserver 8.8.8.8' /etc/network/interfaces"
        os.system(command)
        os.system("sudo sed -i '8c \\ ' /etc/network/interfaces")
        os.system('sudo ifdown eth0')
        os.system('sudo ifup eth0')
    
    def eth1_auto_dns(self):
        command = "sudo sed -i '16c dns-nameserver 8.8.8.8' /etc/network/interfaces"
        os.system(command)
        os.system("sudo sed -i '17c \\ ' /etc/network/interfaces")
        os.system('lsusb | grep "Realtek" | cut -c16,17,18 >/tmp/usb.txt')
        self.usb_id = open('/tmp/usb.txt')
        self.usb_reset = 'sudo python /etc/network/Restusb.py -d ' + self.usb_id.read()