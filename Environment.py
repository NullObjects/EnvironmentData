#! /usr/bin/python3
import Adafruit_DHT
import datetime


class Environment(object):
    '''
        环境(温湿度)传感器
    '''

    def __init__(self, gpio):
        '''
            初始化传感器
        '''
        self.Time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        self.Temperature = 0
        self.Humidity = 0

        self._sensor = Adafruit_DHT.DHT11
        self._gpio = gpio

    def Refresh(self):
        '''
            刷新传感器数据
        '''
        self.Time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        # 获取传感器数据
        humidity, temperature = Adafruit_DHT.read_retry(
            self._sensor, self._gpio)
        if humidity is not None and humidity is not None:
            self.Temperature = round(temperature, 2)
            self.Humidity = round(humidity, 2)
            print(
                '环境温度={0}*C  环境湿度={1}%  Time:{2}'.format(self.Temperature, self.Humidity, self.Time))
        else:
            self.Temperature = 0
            self.Humidity = 0
            print('读取失败，请重试！  Time:{0}'.format(self.Time))


if __name__ == "__main__":
    Environment(17).Refresh()
