# DHT Control
from Device import Device
from Led import LedRGB
from Dht import Dht

device = Device("CFD2EC542D14BBB33902D4DAF53F58CB","6661F3701CC7B71DFCEC6060771C5E158D304EAB5791F1E4D929165BBE3870A7",10000)
device.SYS_CPU_160MHZ()
device.presenceLed(device.GPIO14,device.GPIO12,device.GPIO13,LedRGB.CATODO) # 14 (D5- RED) 12 (D6 - GREEN) 13 (D7 - BLUE)
device.setNetworkConfig('MorseIOT','dudu301011')
device.setDebug(True)

dht = Dht(idtemperature,idhumidity,device.GPIOdht,Dht.DHT22,True,1000)

device.start()

