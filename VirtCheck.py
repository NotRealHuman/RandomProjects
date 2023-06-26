import shutil
import cpuinfo
import wmi

"""This is a very work in progress section of code I've developed for some future malware testing.  The purpose is to 
try and identify if the machine running this code is a virtual machine.  There is still al ot of testing that needs to
occur.  At some point when I have time I will test this agains a series of hypervisors and make changes as needed.

I decided to go via a point system since none of the indicators bellow are a true 100% indicator.  So the idea is that
if the score reaches over 3 its likely an idication that the machine is virtual.  Further indicators will be added as
I learn of them"""

class Virualization_Check:

    def __init__(self):
        self.current_window = None
        self.virt_score = 0

    def disk_check(self):
        """This function checks to determine disk space.  There's a decent chance that if the drive is less than
        50 gigs it's a virutal machine."""
        disk_space, _, _ = shutil.disk_usage("C://")
        disk_space_gb = (disk_space / 1073741824)

        if disk_space_gb < 50:
            self.virt_score += 2

    def cpu_feature_check(self):
        """Checks CPU Features to look for key words that might indicate a Virtual Machine."""
        cpu_features = cpuinfo.get_cpu_info()
        print(cpu_features)

        vm_features = ("hypervisor", "vmx", "svm", "vmm", "nx", "xen")

        if 'flags' in cpu_features:
            flags = cpu_features['flags']
            for feature in vm_features:
                if feature in flags:
                    self.virt_score += 1


    def mac_check(self):
        """Checks agains common standard MAC address's used by some common hypervisors."""
        vm_Macs = ("00:05:69", "00:1C:14", "08:00:27", "0A:00:27", "08:00:27",
                "00:16:3E", "0C:29:AB", "00:1C:42", "00:50:56", "00:0C:29",
                "00:15:5D", "00:03:FF",)
        m = wmi.WMI()
        net_adapt = m.Win32_NetworkAdapterConfiguration(IPEnabled=True)
        target_macs = []

        for adapter in net_adapt:
            target_macs = adapter.MACaddress
            oui = target_macs[:8].upper()

        if oui in vm_Macs:
            self.virt_score += 1

    def virt_determine(self):
        self.disk_check()
        self.mac_check()
        self.cpu_feature_check()

        if self.virt_score > 3:
            print("This machine could be Virtual")
        elif self.virt_score < 3:
            print("It's unlikely the machine is virtual (but not impossible)")
        else:
            print("An error likely occurred in the score calculation")
