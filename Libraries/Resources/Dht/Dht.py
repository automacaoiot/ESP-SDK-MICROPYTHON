from machine import Pin
from dht import DHT11
from dht import DHT22
from Device import Device
from Resource import Resource

class Dht(Resource):

    DHT22 = 22
    DHT11 = 11

    def __init__(self, *args):

        self.refresh = 1000
        self.repeat = True
        self.temperature=None
        self.humidity=None

        if len(args) == 4:
            self.idTemperature = args[0]
            self.idHumidity = args[1]
            self.gpio = args[2]
            self.typeDHT = args[3]
        if len(args) == 5:
            self.idTemperature = args[0]
            self.idHumidity = args[1]
            self.gpio = args[2]
            self.typeDHT = args[3]
            self.repeat = args[4]
        elif len(args) == 6:
            self.idTemperature = args[0]
            self.idHumidity = args[1]
            self.gpio = args[2]
            self.typeDHT = args[3]
            self.repeat = args[4]
            self.refresh = args[5]

        Device.addResource(self,self)
        self.tsDhtBegin = Device.getTime(self)

    @staticmethod
    def start(cls,protocol, url, keyPublic, keySecret,debug):
        try:
            cls.tsDhtNow = Device.getTime(cls)
            if (cls.tsDhtNow - cls.tsDhtBegin) >= (cls.refresh / 1000):
                cls.actionStart(protocol, url, keyPublic, keySecret, debug)
                cls.tsDhtBegin = Device.getTime(cls)
        except:
            pass
        return

    def actionStart(self,protocol, url, keyPublic, keySecret,debug):
        try:
            d = self.measure()
            if d is not None:
                if type(self.temperature) is not float and self.temperature is not None:
                    self.temperature = float(self.temperature)

                if type(d.temperature()) is not float:
                    temperature = float(d.temperature())
                else:
                    temperature = d.temperature()

                if type(self.humidity) is not float and self.humidity is not None:
                    self.humidity = float(self.humidity)

                if type(d.humidity()) is not float:
                    humidity = float(d.humidity())
                else:
                    humidity = d.humidity()

                if self.repeat is False:
                    if self.temperature != temperature and self.humidity != humidity:
                        value=Resource.createFeeds(protocol, url, keyPublic, keySecret,debug, self.idTemperature, str(temperature), self.idHumidity, str(humidity))
                        self.temperature=value[0]
                        self.humidity=value[1]
                    elif self.temperature != temperature:
                        self.temperature=Resource.createFeed(self.idTemperature,protocol, url, keyPublic, keySecret,str(temperature),debug)
                        self.humidity = Resource.lastFeeds(protocol, url, keyPublic, keySecret, self.idHumidity)
                    elif self.humidity != humidity:
                        self.humidity=Resource.createFeed(self.idHumidity,protocol, url, keyPublic, keySecret, str(humidity),debug)
                        self.temperature = Resource.lastFeeds(protocol, url, keyPublic, keySecret, self.idTemperature)
                    else:
                        self.temperature=Resource.lastFeeds(protocol, url, keyPublic, keySecret,self.idTemperature,debug)
                        self.humidity=Resource.lastFeeds(protocol, url, keyPublic, keySecret,self.idHumidity,debug)
                else:
                    value = Resource.createFeeds(protocol, url, keyPublic, keySecret,debug, self.idTemperature, str(temperature),self.idHumidity, str(humidity))
                    self.temperature = value[0]
                    self.humidity = value[1]
        except:
            pass
        return

    def measure(self):
        try:
            print(self.typeDHT)
            if self.typeDHT is 11:
                d = DHT11(Pin(self.gpio))
                d.measure()
                return d
            elif self.typeDHT is 22:
                d = DHT22(Pin(self.gpio))
                d.measure()
                return d
            else:
                return None
        except:
            return None
        return

'''
class Type(object):

    @staticmethod
    def DHT22():
        return 22

    @staticmethod
    def DHT11():
        return 11
'''