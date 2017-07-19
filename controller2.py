import math
import pygame, sys, time
from pygame.locals import *
import serial



pygame.init()
pygame.joystick.init()
joystick = pygame.joystick.Joystick(0)
joystick.init()
screen = pygame.display.set_mode((400,300))
pygame.display.set_caption('Hello World')

#serial communication setup
ser = serial.Serial('/dev/ttyACM0',115200)
outpt = "0,0,"

#controller setup
interval = 0.11

axis = [0.0,0.0,0.0,0.0]


numaxes = joystick.get_numaxes()


numbuttons = joystick.get_numbuttons()


loopQuit = False
while loopQuit == False:

	#Get joystick axes
	outpt = "0,0,"
	for i in range(0,4):
		axis[i] = (joystick.get_axis(i))
	if axis[1] == 0:
		angle = 0
	else:		
		angle = int(math.degrees(math.atan(axis[0]/axis[1]))* -1)
	mag = int(axis[3] * -100)	
	outpt = str(angle) + "," + str(mag)	+ ","  + str(0)
	print(outpt)

        ser.write(outpt)
	time.sleep(.95)
	if(ser.inWaiting() > 0):
		print('read')
	        line = '0'
		line = ser.read(ser.inWaiting())
		print(line)
	#time.sleep(.5)
	 #controller buttons
	#~ outstr = ""
	#~ for i in range(0,numbuttons):
		#~ button = joystick.get_button(i)
		#~ outstr = outstr + str(i) + ":" + str(button) + "|"
	#~ print(outstr)
    
	for event in pygame.event.get():
		if event.type == QUIT:
			loopQuit = True
		elif event.type == pygame.KEYDOWN:
			if event.key == pygame.K_ESCAPE:
				loopQuit = True
           	 

	pygame.display.update()
	time.sleep(interval)

pygame.quit()
sys.exit()
