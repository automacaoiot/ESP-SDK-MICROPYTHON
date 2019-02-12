#Temperature Control
from Device import Device
from Ds1820 import Ds1820
from Led import LedRGB

device = Device("PUBLIC KEY","SECRET KEY")
device.SYS_CPU_240MHZ()
device.presenceLed(device.GPIORED,device.GPIOGREEN,device.GPIOBLUE,LedRGB.CATODO)
device.setNetworkConfig('SSID','PWD')
device.setDebug(True)

ds = Ds1820(IDds1820,device.GPIOds1820,Ds1820.DS18B20,device.CELSIUS,True)

device.start()