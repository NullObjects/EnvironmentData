#! /usr/bin/python3
import os
import datetime


class DeviceStatus(object):
    """
        设备状态
    """

    def __init__(self):
        """
            初始化设备状态
        """
        self.Time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        self.CPUTemperature = 0
        self.CPUOccupancyRate = 0
        self.RAMOccupancyRate = 0
        self.SDCardOccupancyRate = 0
        self.HDDOccupancyRate = 0

    def Refresh(self):
        """
            刷新设备状态
        """
        self.Time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        # 查看CPU温度
        file = open("/sys/class/thermal/thermal_zone0/temp")
        self.CPUTemperature = round(float(file.read()) / 1000, 2)
        file.close()

        # 查看CPU占用率
        self.CPUOccupancyRate = round(float(
            os.popen("top -n1 | awk '/Cpu\(s\):/ {print $2}'").readline().strip()), 2)

        # 查看内存占用率
        ram_stats = self._getRAMinfo()
        self.RAMOccupancyRate = round(
            int(ram_stats[1]) / int(ram_stats[0]) * 100, 2)

        # 查看SD卡占用率
        sd_stats = self._getDiskSpace('/')
        self.SDCardOccupancyRate = float(sd_stats[3].replace('%', ''))

        # 查看HDD占用率
        disk_stats = self._getDiskSpace('/media/ubuntu/Data/')
        self.HDDOccupancyRate = float(disk_stats[3].replace('%', ''))

        print('CPU温度={0}*C  CPU占用率={1}%  内存占用率={2}%'.format(
            self.CPUTemperature, self.CPUOccupancyRate, self.RAMOccupancyRate))
        print('SD卡占用率={0}%  硬盘占用率={1}%  Time:{2}'.format(
            self.SDCardOccupancyRate, self.HDDOccupancyRate, self.Time))

    def _getRAMinfo(self):
        """
            Return RAM information (unit=kb) in a list
            Index 0: total RAM
            Index 1: used RAM
            Index 2: free RAM
        """
        p = os.popen('free')
        i = 0
        while 1:
            i = i + 1
            line = p.readline()
            if i == 2:
                return line.split()[1:4]

    def _getDiskSpace(self, path):
        """
            Return information about disk space as a list (unit included)
            Index 0: total disk space
            Index 1: used disk space
            Index 2: remaining disk space
            Index 3: percentage of disk used
        """
        p = os.popen("df -h " + path)
        i = 0
        while 1:
            i = i + 1
            line = p.readline()
            if i == 2:
                return line.split()[1:5]


if __name__ == '__main__':
    DeviceStatus().Refresh()
