from Api import APIresource
from Device import Device
from Resource import Resource
from machine import Pin

class Rele(Resource):

    OPEN = True
    CLOSED = False

    def __init__(self, *args):

        self.refresh = 1000
        self.countTimeRele = 1
        self.pin = None
        self.state = None

        if len(args) == 3:
            self.id = args[0]
            self.gpio = args[1]
            self.contato = args[2]
        elif len(args) == 4:
            self.id = args[0]
            self.gpio = args[1]
            self.contato = args[2]
            self.refresh = args[3]

        Device.addResource(self,self)
        self.tsReleBegin = Device.getTime(self)

    @staticmethod
    def start(cls, protocol, url, keyPublic, keySecret,debug):
        try:
            if(Resource.resourceTime(Device.getTime(cls),cls.tsReleBegin,cls.refresh)):
                response,statusCode=APIresource.resourceLastFeeds(protocol, url, keyPublic, keySecret, cls.id, debug)
                cls.actionStart(response,statusCode)
                cls.tsReleBegin = Device.getTime(cls)
        except:
            pass
        return

    def actionStart(self,response,statusCode):
        try:
            if self.pin is None:
                self.pin = Pin(self.gpio, Pin.OUT)

            if statusCode == 200:
                self.actionRele(response)
            else:
                self.actionReleOff()
        except:
            pass
        return

    def actionRele(self, response):
        try:
            if response['payload'] is not None:
                if (response['success']) is True:
                    state = int(response['payload']['raw_data'])
                    if state is 1 or state is 0:
                        if state != self.state:
                            if self.contato is Rele.OPEN:
                                self.contatoOpen(state)
                            else:
                                self.contatoClosed(state)
                            self.state = state
                return
            self.actionReleOff()
        except:
            pass
        return

    def actionReleOff(self):
        try:
            if self.contato is Rele.OPEN:
                self.pin.value(1)
            else:
                self.pin.value(0)
            self.state = None
        except:
            pass
        return

    def contatoClosed(self,state):
        try:
            if int(state) is 0:
                self.pin.value(0)
            else:
                self.pin.value(1)
        except:
            pass
        return

    def contatoOpen(self,state):
        try:
            if int(state) is 0:
                self.pin.value(1)
            else:
                self.pin.value(0)
        except:
            pass
        return