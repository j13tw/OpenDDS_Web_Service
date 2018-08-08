import os, sys
import glob

class File_search():
    def __init__(self):
        pass

    def ini_list(self):
        self.ini_table = glob.glob('/etc/network/*')
        for x in range(0, len(self.ini_table)):
            self.ini_table[x] = self.ini_table[x].split('/')[3]
        return  self.ini_table

class Time_config():
    def __init__(self):
        pass

    def date_set(self, year, month, date):
        self.date_command = 'sudo date -s ' + year + month + date
        os.system(self.date_command)
    
    def time_set(self, hour, minute, second):
        self.time_command = 'sudo date -s ' + hour + ':' + minute + ':' + second
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