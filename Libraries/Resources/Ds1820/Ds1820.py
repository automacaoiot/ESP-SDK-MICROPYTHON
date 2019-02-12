from machine import Pin
import time
from ds18x20 import DS18X20
from onewire import OneWire
from Device import Device
from Resource import Resource
from Api import APIresource
import sys

class Ds1820(Resource):

    DS18X20 = 0
    DS18B20 = 1

    def __init__(self, *args):

        self.refresh = 1000
        self.repeat = True
        self.temperaturePast=None
        self.sleepDS18B20 = 1000
        self.timeTicket = time.ticks_ms()

        if len(args) == 4:
            self.idTemperature = args[0]
            self.gpio = args[1]
            self.typeDS = args[2]
            self.scale = args[3]
        if len(args) == 5:
            self.idTemperature = args[0]
            self.gpio = args[1]
            self.typeDS = args[2]
            self.scale = args[3]
            self.repeat = args[4]
        elif len(args) == 6:
            self.idTemperature = args[0]
            self.gpio = args[1]
            self.typeDS = args[2]
            self.scale = args[3]
            self.repeat = args[4]
            self.refresh = args[5]

        Device.addResource(self,self)
        self.tsDSBegin = Device.getTime(self)

    @staticmethod
    def start(cls,protocol, url, keyPublic, keySecret,debug):
        try:
            if (Resource.resourceTime(Device.getTime(cls), cls.tsDSBegin, cls.refresh)):
                cls.actionStart(protocol, url, keyPublic, keySecret, debug)
                cls.tsDSBegin = Device.getTime(cls)
        except:
            pass
        return

        # cls.tsDSNow = Device.getTime(cls)
        # if (cls.tsDSNow - cls.tsDSBegin) >= (cls.refresh / 1000):
        #     cls.actionStart(protocol, url, keyPublic, keySecret, debug)
        #     cls.tsDSBegin = Device.getTime(cls)
        # return

    def actionStart(self,protocol, url, keyPublic, keySecret,debug):
        try:
            ds = DS18X20(OneWire(Pin(self.gpio)))
            roms = ds.scan()
            ds.convert_temp()
            for rom in roms:
                temp = ds.read_temp(rom)

            self.temperatureNow = temp
            Device.delayTicket(self.sleepDS18B20,self.timeTicket)
            if self.scale:
                self.temperatureNow=self.c_to_f(self.temperatureNow)

            if type(self.temperaturePast) is not float and self.temperaturePast is not None:
                self.temperaturePast = float(self.temperaturePast)

            if type(self.temperatureNow) is not float:
                self.temperatureNow = float(self.temperatureNow)

            Device.delayTicket(self.sleepDS18B20, self.timeTicket)

            if self.repeat is False:
                if self.temperatureNow != self.temperaturePast:
                    value = Resource.createFeed(self.idTemperature, protocol, url, keyPublic, keySecret,
                                                self.temperatureNow, debug)
                    self.temperaturePast = value
                else:
                    value = Resource.lastFeeds(protocol, url, keyPublic, keySecret, self.idTemperature, debug)
                    self.temperaturePast = value
            else:
                value = Resource.createFeed(self.idTemperature, protocol, url, keyPublic, keySecret, self.temperatureNow,
                                    debug)
                self.temperaturePast = value
        except:
            pass
        return

    def c_to_f(self,c):
        """
        Converts Celsius to Fahrenheit
        :param c: Temperature in Celsius
        :type c: float
        :return: Temperature in Fahrenheit
        :rtype: float
        """
        try:
            return (c * 1.8) + 32
        except:
            pass
        return 0