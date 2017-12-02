import subprocess
import re
import shutil
import threading

class Piwify:
    def __init__(self, wifi="wlan0"):
        self.wifi = wifi
        self.wifi_list = []


    def get_wifi_list(self):
        cmd = [ "sudo", "iwlist", self.wifi, "scan" ]
        cells = self.run_command(cmd)
        self.parsh_cells(cells)
        return self.wifi_list


    def run_command(self, cmd):
        p = subprocess.Popen(cmd, stdout=subprocess.PIPE)
        return p.communicate()[0]


    def parsh_cells(self, cells):
        qaddr = re.compile('.*Address: (.*)')
        qchan = re.compile('.*Channel:(.*)')
        qname = re.compile('.*ESSID:\"(.*)\"')
        qqual = re.compile('.*Quality=(.*)\/.*')
        qencr = re.compile('.*Encryption key:(.*)')
        addr, chan, name, qual, encr = "", "", "", "", ""
        for line in cells.splitlines():
            m = qaddr.match(line)
            if m:
                addr=m.group(1)
            m = qchan.match(line)
            if m:
                chan = m.group(1)
            m = qqual.match(line)
            if m:
                qual = m.group(1)
            m = qencr.match(line)
            if m:
                encr = m.group(1)
            m = qname.match(line)
            if m:
                name = m.group(1)
                self.add_to_wifi(name, addr, chan, qual, encr)

    def get_wifi(self):
        return self.wifi_list


    def add_to_wifi(self, name, address, channel, quality, enc):
        self.wifi_list.append({"name": name, "address": address,
                               "channel": channel, "quality": quality,
                               "enc": enc})

    def reboot(self):
        sudo_reboot = ["sudo", "reboot"]
        self.run_command(sudo_reboot)

    def reboot_timer(self, time):
        t = threading.Timer(time, self.reboot)
        t.start()

    def add_wpa_config(self, ssid, key, address=None):
        '''wpa_supplicant.conf  network={
	ssid="STILLNOTFORYOU"
	psk="a123456789"
	key_mgmt=WPA-PSK
    }'''
        config = """network={
	ssid=\""""+ssid+"""\"
	psk=\""""+key+"""\"
}"""
        shutil.copy2('/etc/wpa_supplicant/wpa_supplicant.conf','/tmp/wpa_supplicant.conf')
        with open('/tmp/wpa_supplicant.conf', "a") as myfile:
            myfile.write(config)
        sudo_cp = ["sudo", "cp", "/tmp/wpa_supplicant.conf", "/etc/wpa_supplicant/wpa_supplicant.conf"]
        self.run_command(sudo_cp)

    def enable_camera(self):
        sudo_enable_camera = [ "sudo", "./enable_camera.sh" ]
        self.run_command(sudo_enable_camera)

    def enable_ssh(self, sshpass):
        sudo_enable_ssh = ["sudo", "./enable_ssh.sh", sshpass]
        self.run_command(sudo_enable_ssh)

    def domain_prefix(self, domain_prefix):
        sudo_domain_prefix = ["sudo", "./domain_prefix.sh", domain_prefix]
        self.run_command(sudo_domain_prefix)

    def disable_overscan(self):
        sudo_disable_overscan = [ "sudo", "./disable_overscan.sh"]
        self.run_command(sudo_disable_overscan)

#pi = Piwify("wlp3s0")
#for cell in pi.get_wifi_list():
#    print(cell)

"""Cell 01 - Address: 00:20:A6:95:B4:5F
                    Channel:13
                    Frequency:2.472 GHz (Channel 13)
                    Quality=68/70  Signal level=-42 dBm  
                    Encryption key:on
                    ESSID:"KUKURIBALA"
"""