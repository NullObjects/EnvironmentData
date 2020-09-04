#! /usr/bin/python3
import Environment
import DeviceStatus
import json
import time
import pymysql


class UPloadData(object):
    '''
        上传数据
    '''

    def __init__(self, interval):
        '''
            初始化上传
        '''
        if(self._DBInit() == False):
            print('数据库连接失败，请检查连接')
            return
        self.Sensor = Environment.Environment(17)
        self.Device = DeviceStatus.DeviceStatus()
        while True:
            print('>>>  Start  <<<')
            self._UPload()
            time.sleep(interval)

    def _DBInit(self):
        '''
        数据库连接初始化
        '''
       # 新建连接
        with open('config.json') as configJson:
            config = json.load(configJson)
        dbConfig = config['connections'][int(config['connectionSelect'])]
        try:
            self._connection = pymysql.connect(host=dbConfig['host'],
                                               database=dbConfig['database'],
                                               user=dbConfig['user'],
                                               password=dbConfig['password'])
            return True
        # 连接字典错误
        except Exception as ex:
            print('Exception:\n' + str(ex))
            return False

    def _UPload(self):
        '''
            数据上传数据库
        '''
        self.Sensor.Refresh()
        self.Device.Refresh()
        cursor = self._connection.cursor()
        try:
            if(self.Sensor.Temperature != 0 and self.Sensor.Humidity != 0):
                cursor.execute("INSERT INTO Environment(Temperature, Humidity, RecordTime) VALUES({0}, {1}, '{2}')".format(
                    self.Sensor.Temperature, self.Sensor.Humidity, self.Sensor.Time))
            cursor.execute(
                "INSERT INTO DeviceStatus(CPUTemperature, CPUOccupancyRate, RAMOccupancyRate, SDCardOccupancyRate, HDDOccupancyRate, RecordTime) VALUES({0}, {1}, {2}, {3}, {4}, '{5}')".format(
                    self.Device.CPUTemperature,
                    self.Device.CPUOccupancyRate,
                    self.Device.RAMOccupancyRate,
                    self.Device.SDCardOccupancyRate,
                    self.Device.HDDOccupancyRate,
                    self.Device.Time))
            self._connection.commit()
        except Exception as ex:
            print("UPload Error:\n" + str(ex))
            self._connection.rollback()
        cursor.close()


if __name__ == "__main__":
    with open('config.json') as configJson:
        config = json.load(configJson)
    UPloadData(int(config['TimerInterval']))
