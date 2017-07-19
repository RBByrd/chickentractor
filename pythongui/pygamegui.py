import pygame, sys, time
import math
from pygame.locals import *
import serial
import os.path
import os

#Start the pygame set
pygame.init()

#set the window note 480X320 is the size of the touch screen
displayWidth = 480
displayHeight = 320
buttonScale  = 6

setFont = 'freesansbold.ttf'

#set up colors for use
#red
warningTextColor = (255,0,0)
#black
butTextColor = (0,0,0)
#white
staticColor = (255,255,255)
#blue
pressedColor = (0,0,255)
#black
background = (0,0,0)

#display used with touch screen as fullscreen
#gameDisplay = pygame.display.set_mode((displayWidth,displayHeight), pygame.FULLSCREEN, 0)

endMode = 1

#display used for troubleshoot non fullscreen
gameDisplay = pygame.display.set_mode((displayWidth,displayHeight), 0, 0)



clock = pygame.time.Clock()

def text_objects(text,font, textColor, xyPos):
	textSurface = font.render(text, True, textColor)
	TextRect = textSurface.get_rect()
	TextRect.center = (xyPos[0] , xyPos[1])
	gameDisplay.blit(textSurface,TextRect)


def button(xyPos, text, color):
	
	#dimensions of the button and creation
	topX = xyPos[0] - (displayWidth/buttonScale)
	topY = xyPos[1] - (displayHeight/buttonScale)
	rectW = (displayWidth/buttonScale) * 2
	rectH = (displayHeight/buttonScale) * 2
	pygame.draw.rect(gameDisplay, color, [ topX , topY , rectW , rectH])
	
	#Button text creation
	buttonText = pygame.font.Font(setFont,15)
	text_objects(text, buttonText, butTextColor, xyPos)

def butDim(xyPos):
	topX = xyPos[0] - (displayWidth/buttonScale)
	topY = xyPos[1] - (displayHeight/buttonScale)
	botX = xyPos[0] + (displayWidth/buttonScale)
	botY = xyPos[1] + (displayHeight/buttonScale)
	return topX, botX, topY, botY

def drawMotion(pos, radius, deg, mag):
	endPos = [0,0]
	deg = deg - 90
	length = (mag * radius)/100
	endPos[0] = int((math.cos(math.radians(deg)) * length) + pos[0])
	endPos[1] = int((math.sin(math.radians(deg)) * length) + pos[1])
	pygame.draw.circle(gameDisplay, staticColor, pos, radius, 0)
	pygame.draw.line(gameDisplay, pressedColor, pos, endPos, 6)
	

def manualMode():
	pygame.joystick.init()
	joystick = pygame.joystick.Joystick(0)
	joystick.init()
	print(pygame.joystick.get_count())
    
	chrZero = bytes(0)
	
	gameDisplay.fill(background)
	
	#button and prompts for no controller
	warningPos = [(displayWidth/2), (displayHeight/4)]
	butmid1 = [(displayWidth/2), (3*displayHeight/4)]
	butdim1 = butDim(butmid1)
	button1Color = staticColor
	
	#button for working function
	butmid2 = [(displayWidth/4), (displayHeight/2)]
	butdim2 = butDim(butmid2)
	button2Color = staticColor
	
	directionMid = [(3*displayWidth/4), (displayHeight/2)]
	
	loopQuit = False
	
	while (pygame.joystick.get_count() == 0):
		warningFont = pygame.font.Font(setFont,55)
		text_objects('No Controller Detected',warningFont, warningTextColor, warningPos)
		button(butmid1, 'Main Menu', button1Color)
		
		#looking for user input
		for event in pygame.event.get():
			#mouse (touch) input checking for press and release within button regions		
			if event.type == pygame.MOUSEBUTTONDOWN:
				if event.button == 1:
					if (event.pos[0] > butdim1[0]) & (event.pos[0] < butdim1[1]):
						if (event.pos[1] > butdim1[2]) & (event.pos[1] < butdim1[3]):
							button1Color = pressedColor						
			elif event.type == pygame.MOUSEBUTTONUP:
				if event.button == 1:
					if (event.pos[0] > butdim1[0]) & (event.pos[0] < butdim1[1]):
						if (event.pos[1] > butdim1[2]) & (event.pos[1] < butdim1[3]):
							gameDisplay.fill(background)
							loopQuit = True
							break						
		pygame.display.update()
		print(pygame.joystick.get_count())
	
	#serial communication setup
	#ser = serial.Serial('/dev/ttyACM0',115200)
	outpt = chrZero + chrZero

	#controller setup
	interval = 0.11
	axis = [0.0,0.0,0.0,0.0]
	numaxes = joystick.get_numaxes()
	numbuttons = joystick.get_numbuttons()


	
	while loopQuit == False:
		
		
		button(butmid2, 'Main Menu', button2Color)

		#Get joystick axes
		outpt = chrZero + chrZero
		for i in range(0,4):
			axis[i] = (joystick.get_axis(i))
		if axis[1] == 0:
			angle = 0
		else:		
			angle = int(math.degrees(math.atan(axis[0]/axis[1]))* -1) & 255
		mag = int(axis[3] * -100) & 255
		outpt = chr(angle) + chr(mag)
		#Get button inputs
		B = 3
		for i in range(8,12):
			buttonInput = joystick.get_button(i)
			B = B * 2
			B = B | buttonInput
		outpt = outpt + chr(B)
		print(B)
		if arduino0 == 'P':
			ser0.write(outpt)
		
			drawMotion(directionMid, (displayWidth/4), angle, mag) 
		
			time.sleep(.95)
			if(ser0.inWaiting() > 0):
				print('read')
				line = '0'
				line = ser0.read(ser0.inWaiting())
				print(line)
			#time.sleep(.5)
		elif arduino1 == 'P':
			ser1.write(outpt)
		
			drawMotion(directionMid, (displayWidth/4), angle, mag) 
		
			time.sleep(.95)
			if(ser1.inWaiting() > 0):
				print('read')
				line = '0'
				line = ser1.read(ser1.inWaiting())
				print(line)
			#time.sleep(.5)

		for event in pygame.event.get():
			if event.type == QUIT:
				loopQuit = True
			elif event.type == pygame.MOUSEBUTTONDOWN:
				if event.button == 1:
					if (event.pos[0] > butdim2[0]) & (event.pos[0] < butdim2[1]):
						if (event.pos[1] > butdim2[2]) & (event.pos[1] < butdim2[3]):
							button2Color = pressedColor						
			elif event.type == pygame.MOUSEBUTTONUP:
				if event.button == 1:
					if (event.pos[0] > butdim2[0]) & (event.pos[0] < butdim2[1]):
						if (event.pos[1] > butdim2[2]) & (event.pos[1] < butdim2[3]):
							button2Color = staticColor
							gameDisplay.fill(background)
							loopQuit = True	
				 
		pygame.display.update()
		time.sleep(interval)
	pygame.joystick.quit()

def main(running):
	
	#set buttons to static color
	button1Color = staticColor
	button2Color = staticColor
	button3Color = staticColor
	button4Color = staticColor
	
	#get mid positions for buttons and text butmid[x,y]
	butmid1  = [(displayWidth/4), (displayHeight/4)]
	butmid2  = [(3*displayWidth/4), (displayHeight/4)]
	butmid3  = [(displayWidth/4), (3*displayHeight/4)]
	butmid4  = [(3*displayWidth/4), (3*displayHeight/4)]
	
	#get button dimensions butdim[xlow,xhigh,ylow,yhigh]
	butdim1 = butDim(butmid1) 
	butdim2 = butDim(butmid2)
	butdim3 = butDim(butmid3)
	butdim4 = butDim(butmid4)
	
	
	#main loop for the gui
	while running:
		
		#declare and create buttons
		button(butmid1, 'Manual Mode', button1Color)
		button(butmid2, 'Automatic Mode', button2Color)
		button(butmid3, 'Settings', button3Color)
		button(butmid4, 'Shutdown', button4Color)
		
		#looking for user input
		for event in pygame.event.get():
			#keyboard input
			if event.type == pygame.KEYDOWN:
				#exit out of the program by pressing 'esc' 
				if event.key == 27:
					running = False
			#mouse (touch) input checking for press and release within button regions		
			elif event.type == pygame.MOUSEBUTTONDOWN:
				if event.button == 1:
					if (event.pos[0] > butdim1[0]) & (event.pos[0] < butdim1[1]):
						if (event.pos[1] > butdim1[2]) & (event.pos[1] < butdim1[3]):
							button1Color = pressedColor	
						elif (event.pos[1] > butdim3[2]) & (event.pos[1] < butdim3[3]):
							button3Color = pressedColor	
					elif (event.pos[0] > butdim2[0]) & (event.pos[0] < butdim2[1]):
						if (event.pos[1] > butdim2[2]) & (event.pos[1] < butdim2[3]):
							button2Color = pressedColor	
						elif (event.pos[1] > butdim4[2]) & (event.pos[1] < butdim4[3]):							
							button4Color = pressedColor					
			elif event.type == pygame.MOUSEBUTTONUP:
				if event.button == 1:
					if (event.pos[0] > butdim1[0]) & (event.pos[0] < butdim1[1]):
						if (event.pos[1] > butdim1[2]) & (event.pos[1] < butdim1[3]):
							button1Color = staticColor
							gameDisplay.fill(background)	
							manualMode()
						elif (event.pos[1] > butdim3[2]) & (event.pos[1] < butdim3[3]):
							button3Color = staticColor	
					elif (event.pos[0] > butdim2[0]) & (event.pos[0] < butdim2[1]):
						if (event.pos[1] > butdim2[2]) & (event.pos[1] < butdim2[3]):
							button2Color = staticColor	
						elif (event.pos[1] > butdim4[2]) & (event.pos[1] < butdim4[3]):							
							running = False	
					else:
						button1Color = staticColor	
						button2Color = staticColor
						button3Color = staticColor
						button4Color = staticColor
			#print(event)
		pygame.display.update()	

def serialSetup(arduino0, arduino1):
	
	#button and pormpts for missing arduino and syncing arduinos
	warningPos1 = [(displayWidth/2), (displayHeight/8)]
	warningPos2 = [(displayWidth/2), (2*displayHeight/8)]
	butmid1 = [(displayWidth/2), (3*displayHeight/4)]
	butdim1 = butDim(butmid1)
	button1Color = staticColor
		
	
	#check for the arduinos
	connected0 = os.path.exists('/dev/ttyACM0')
	connected1 = os.path.exists('/dev/ttyACM1')
	
	#let the user know if arduinos are not found and continue to look for them
	while not (connected0 & connected1):
		
		#Create button and text
		warningFont = pygame.font.Font(setFont,35)
		text_objects('1 and/or 2 Arduinos',warningFont, warningTextColor, warningPos1)
		text_objects('are not Detected!',warningFont, warningTextColor, warningPos2)		
		button(butmid1, 'Shutdown', button1Color)
		
		#Test for arduinos until both are found
		connected0 = os.path.exists('/dev/ttyACM0')
		connected1 = os.path.exists('/dev/ttyACM1')
		
		#looking for user input
		for event in pygame.event.get():
			#mouse (touch) input checking for press and release within button regions		
			if event.type == pygame.MOUSEBUTTONDOWN:
				if event.button == 1:
					if (event.pos[0] > butdim1[0]) & (event.pos[0] < butdim1[1]):
						if (event.pos[1] > butdim1[2]) & (event.pos[1] < butdim1[3]):
							button1Color = pressedColor						
			elif event.type == pygame.MOUSEBUTTONUP:
				if event.button == 1:
					if (event.pos[0] > butdim1[0]) & (event.pos[0] < butdim1[1]):
						if (event.pos[1] > butdim1[2]) & (event.pos[1] < butdim1[3]):
							gameDisplay.fill(background)
							shutDown(endMode)
		pygame.display.update()
	
	
	time.sleep(1)
	gameDisplay.fill(background)
	ser0 = serial.Serial('/dev/ttyACM0',9600)
	ser1 = serial.Serial('/dev/ttyACM1',9600)
	
	while not ((arduino0 == 'G' and arduino1 == 'P') or (arduino0 == 'P' and arduino1 == 'G')):
		time.sleep(1)
		if(ser0.inWaiting() > 0):
			arduino0 = ser0.read(ser0.inWaiting())
			print(arduino0)
		if(ser1.inWaiting() > 0):
			arduino1 = ser1.read(ser1.inWaiting())
			print(arduino1)
		#Create button and text
		warningFont = pygame.font.Font(setFont,35)
		text_objects('Syncing',warningFont, warningTextColor, warningPos1)
		text_objects('Arduinos',warningFont, warningTextColor, warningPos2)		
		button(butmid1, 'Shutdown', button1Color)
		
		#looking for user input
		for event in pygame.event.get():
			#mouse (touch) input checking for press and release within button regions		
			if event.type == pygame.MOUSEBUTTONDOWN:
				if event.button == 1:
					if (event.pos[0] > butdim1[0]) & (event.pos[0] < butdim1[1]):
						if (event.pos[1] > butdim1[2]) & (event.pos[1] < butdim1[3]):
							button1Color = pressedColor						
			elif event.type == pygame.MOUSEBUTTONUP:
				if event.button == 1:
					if (event.pos[0] > butdim1[0]) & (event.pos[0] < butdim1[1]):
						if (event.pos[1] > butdim1[2]) & (event.pos[1] < butdim1[3]):
							gameDisplay.fill(background)
							shutDown(endMode)
						else:
							button1Color = staticColor
					else:
						button1Color = staticColor
						
		pygame.display.update()
		
	for i in range(10):
		ser0.write('Y')
		ser1.write('Y')
		time.sleep(1)
		
	gameDisplay.fill(background)
	return 	arduino0, arduino1, ser0, ser1

def shutDown(endMode):
	if endMode == 1:
		pygame.quit()
		quit()
	elif endMode == 2:
		os.system('shutdown now -h')
		

		
#variable used to continue to run the gui
running = True

arduino0 = 'n'
arduino1 = 'n'

arduino0, arduino1, ser0, ser1 = serialSetup(arduino0, arduino1)			
main(running)

shutDown(endMode)

				

