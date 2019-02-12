# Rele Control
from Device import Device
from Rele import Rele
from Led import LedRGB

device = Device("PUBLIC KEY","SECRET KEY",10000)
device.SYS_CPU_160MHZ()
device.presenceLed(device.GPIORED,device.GPIOGREEN,device.GPIOBLUE,LedRGB.CATODO)
device.setNetworkConfig('SSID','PWD')
device.setDebug(True)

rele = Rele(IDrele, device.GPIOrele, Rele.OPEN, 1000)

device.start()

