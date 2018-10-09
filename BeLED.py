#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# NeoPixel library strandtest example
# Author: Tony DiCola (tony@tonydicola.com)
#
# Direct port of the Arduino NeoPixel library strandtest example.  Showcases
# various animations on a strip of NeoPixels.

# Music: download lyrics if possible and show them.

import time
from neopixel import *
import argparse

from BeFont_x_6 import getCharArray_x_6
from BeFont_x_6 import buildTextArray_x_6
font_render = buildTextArray_x_6('Hey Süsse, bock aufn Kaffee ;)? Der Himmel hat angerufen, es fehlt ein Engel blahblah blah und so weiter.... :)')

# BeLED screen configuration
# The screen can have "lights" before and after it on the same line, for lighting other stuff, too, like a power LED.
SCREEN_COUNT_PRE 	= 1		# Number of LEDs before the actual screen.
SCREEN_COUNT_X 		= 10	# Number of LEDs in one line on the screen.
SCREEN_COUNT_Y		= 10	# Number of lines on the screen.
SCREEN_COUNT_AFT	= 0		# Number of LEDs after the actual screen.
SCREEN_DIRECTION 	= 1     # 0 = normal, 1 = y flip, 2 = x flip, 3 = x & y flip
							# This is used for the renderArray function to determine which side of the array faces up.
							# Needed for rendering the fonts in the right direction, my setup is "wrong" for y so I use 1 here.
#SCREEN_ORIENTATION = 0		# 0 = "north", 1 = "south", 2 = "east", 3 = "west"
							# even if the screen is flipped right, it may be turned into the wrong direction.
							# we turn it with this function.

# LED strip configuration:
PIXELWAITTIME = 50*0.001
LED_COUNT      = SCREEN_COUNT_PRE + (SCREEN_COUNT_X * SCREEN_COUNT_Y) + SCREEN_COUNT_AFT  # Number of LED pixels.
LED_PIN        = 18      # GPIO pin connected to the pixels (18 uses PWM!).
#LED_PIN        = 10      # GPIO pin connected to the pixels (10 uses SPI /dev/spidev0.0).
LED_FREQ_HZ    = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA        = 10      # DMA channel to use for generating signal (try 10)
LED_BRIGHTNESS = 55     # Set to 0 for darkest and 255 for brightest
LED_INVERT     = False   # True to invert the signal (when using NPN transistor level shift)
LED_CHANNEL    = 0       # set to '1' for GPIOs 13, 19, 41, 45 or 53

def wheel(pos):
	"""Generate rainbow colors across 0-255 positions."""
	if pos < 85:
		return Color(pos*3, 255-pos*3,0)
	elif pos < 170:
		pos -= 85
		return Color(255-pos*3,0,pos*3)
	else:
		pos-=170
		return Color(0,pos*3,255-pos*3)

j = 0
maxJ = 256
def rainbowCycle(strip, maskarray):
	"""Draw rainbow that uniformly distributes itself across all pixels."""
	global j
	global maxJ
	for i in range(strip.numPixels()):
		if i>=SCREEN_COUNT_PRE and i<SCREEN_COUNT_PRE+SCREEN_COUNT_X*SCREEN_COUNT_Y:
			maskpos = i-SCREEN_COUNT_PRE
			if maskpos>=0 and maskpos<len(maskarray):
				if maskarray[maskpos]!=0:
					strip.setPixelColor(i,wheel((int(i*256/strip.numPixels())+j)&255))
	j=j-5
	if j<=0:
		j=maxJ+j

###### RENDER FUNCTIONS ##########################
def renderBackground(strip):
	#rainbowCycle(strip)
	clearScreen(strip)
	return 0

foregroundx=SCREEN_COUNT_X+1
oldtime= -1
timearray = buildTextArray_x_6("0")
txt_width=0
def renderForeground(strip):
	global foregroundx
	global oldtime
	global txt_width
	global timearray
	
	# get the current time.
	currenttime = time.ctime(time.time())
	if(oldtime!=currenttime):
		# maybe build a new time array.
		timearray = buildTextArray_x_6(currenttime)
		print("Time:"+currenttime)
		oldtime = currenttime
		txt_width = len(timearray[0])

	mask = createFlatScreenMask(timearray,foregroundx,2)
	rainbowCycle(strip, mask)
	foregroundx=foregroundx-1
	# reset text position
	if foregroundx <= -txt_width:
		foregroundx=SCREEN_COUNT_X+1

	return 0
	
# render a screenarray to a mask with the size of the strip screen.
def createScreenMask(screenarray,x,y):
	"""Create a mask (buffer) in screen size and put the screen array on it."""
	screenend = LED_COUNT-(SCREEN_COUNT_PRE + (SCREEN_COUNT_X * SCREEN_COUNT_Y))
	
	# create the screen buffer and clear it.
	returnarray = []
	for cy in range(SCREEN_COUNT_Y):
		returnarray.append([])
		for cx in range(SCREEN_COUNT_X):
			returnarray[cy].append(0)
	
	# go through the screen pixels
	# and create the mask on the returnarray.
	for sy in range(SCREEN_COUNT_Y):
		for sx in range(SCREEN_COUNT_X):
			# pixelpos is the real screen position
			if SCREEN_DIRECTION==0:
				ppX =sx
				ppY =sy
			# flip only y
			if SCREEN_DIRECTION==1:
				ppX = sx
				ppY = SCREEN_COUNT_Y-sy-1
			# flip only x
			if SCREEN_DIRECTION==2:
				ppX = SCREEN_COUNT_X-sx-1
				ppY = sy
			# flip x and y
			if SCREEN_DIRECTION==3:
				ppX = SCREEN_COUNT_X-sx-1
				ppY = SCREEN_COUNT_Y-sy-1
			# check if the position is on the screen.
			if ppX>=0 and ppY>=0 and ppX<SCREEN_COUNT_X and ppY<SCREEN_COUNT_Y:
				# get the position on the screenarray
				tx = sx - x
				ty = sy - y
				setpix = -1
				if len(screenarray)>ty and ty>=0:
					if len(screenarray[ty])>tx and tx>=0:
						setpix = screenarray[ty][tx]
				# set the right color
				#col = Color(0,127,0)
				# blank pixel gets background color.
				# if setpix == 0:
				#	col = Color(0,0,0)
				# coloured pixel gets foreground color.
				if setpix != -1:
					returnarray[ppY][ppX]=setpix
	
	return returnarray

# create a one dimensional screen mask.
def createFlatScreenMask(screenarray,x,y):
	mask = createScreenMask(screenarray, x,y)
	ret = []
	for y in range(len(mask)):
		for x in range(len(mask[y])):
			ret.append(mask[y][x])
	return ret

# render a screenarray onto the strip.
def renderArray(strip, screenarray, x, y):
	"""Render the screenarray onto the strip."""
	screenend = LED_COUNT-(SCREEN_COUNT_PRE + (SCREEN_COUNT_X * SCREEN_COUNT_Y))
	# go through the screen pixels
	for sy in range(SCREEN_COUNT_Y):
		for sx in range(SCREEN_COUNT_X):
			# pixelpos is the real screen position
			if SCREEN_DIRECTION==0:
				pixelpos = SCREEN_COUNT_PRE + sy*SCREEN_COUNT_X+sx
			# flip only y
			if SCREEN_DIRECTION==1:
				pixelpos = SCREEN_COUNT_PRE + (SCREEN_COUNT_Y-sy-1)*SCREEN_COUNT_X+sx
			# flip only x
			if SCREEN_DIRECTION==2:
				pixelpos = SCREEN_COUNT_PRE + (sy+1)*SCREEN_COUNT_X-sx-1
			# flip x and y
			if SCREEN_DIRECTION==3:
				pixelpos = SCREEN_COUNT_PRE + (SCREEN_COUNT_Y-sy)*SCREEN_COUNT_X-sx-1
			if pixelpos<strip.numPixels() and pixelpos>=0:
				# get the position on the screenarray
				tx = sx - x
				ty = sy - y
				setpix = -1
				if len(screenarray)>ty and ty>=0:
					if len(screenarray[ty])>tx and tx>=0:
						setpix = screenarray[ty][tx]
				# set the right color
				#col = Color(0,127,0)
				# blank pixel gets background color.
				# if setpix == 0:
				#	col = Color(0,0,0)
				# coloured pixel gets foreground color.
				if setpix == 1:
					col = Color(150,255,0)
					# set the color on the screen.	
					strip.setPixelColor(pixelpos, col)

# clear all pixels
def clearScreen(strip):
	"""Clear all pixels on the screen."""
	for i in range(strip.numPixels()):
		strip.setPixelColor(i, Color(0,0,0))
	strip.show()

# Main program logic follows:
if __name__ == '__main__':
    # Process arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--clear', action='store_true', help='clear the display on exit')
    args = parser.parse_args()

    # Create NeoPixel object with appropriate configuration.
    strip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL)
    # Intialize the library (must be called once before other functions).
    strip.begin()
	
    print ('Press Ctrl-C to quit.')
    if not args.clear:
        print('Use "-c" argument to clear LEDs on exit')
	
    try:
		while True:
			#renderArray(strip,font_render,px,2)
			# render the background.
			renderBackground(strip)
			# render the foreground.
			renderForeground(strip)
			
			# finally show the strip and wait some time.
			strip.show()
			time.sleep(PIXELWAITTIME)

    except KeyboardInterrupt:
        if args.clear:
            clearScreen(strip)
