from time import sleep
from UUGear import *
 
device = UUGearDevice('UUGear-Arduino-8712-8646')
 
if device.isValid():
    device.setPinModeAsOutput(13)
    for i in range(5):
        device.setPinHigh(13)
        sleep(0.2)
        device.setPinLow(13)
        sleep(0.2)
 
    device.setPinModeAsInput(9)
    print 'Pin 9 status=', device.getPinStatus(9)
 
    device.detach()
    device.stopDaemon()
else:
    print 'UUGear device is not correctly initialized.'