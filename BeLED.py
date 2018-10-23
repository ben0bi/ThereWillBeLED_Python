#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# NeoPixel library strandtest example
# Author: Tony DiCola (tony@tonydicola.com)
#
# Heavily edited by ben0bi for using the BeLED library.
#
# Direct port of the Arduino NeoPixel library strandtest example.  Showcases
# various animations on a strip of NeoPixels.

# Target (Problems to solve, not related to LEDs):
# 	Get song name from (remote) mopidy server. Server can use a script.
#		It is not possible to use LEDs and mopidy on the same raspberry.
#		So I use 2 raspis, one for playing music and one for fancy LED stuff.
#		The second one should be notified when the song on the first one changes.
#		It should download and show the song name and other information when the user presses a (GPIO-)button.
# Nice-To-Have for Music: download lyrics if possible and show them.

import time
from neopixel import *
import argparse

from BeLEDLib import *

from BeFont_x_6 import getCharArray_x_6
from BeFont_x_6 import buildTextArray_x_6
#font_render = buildTextArray_x_6('Dr Beni het Sex und zwar JETZ, mit Fraue woner cha vertraue und trotzdem versaue!')
#font_render = buildTextArray_x_6('ben0biTech Incorporated & Co. KG bedankt sich herzlich bei allen Nichtmitarbeitern für ihre Unterstützung! *Danki Sähr*')
font_render = buildTextArray_x_6('III: Gaia    ')

# LED strip configuration:
PIXELWAITTIME = 40*0.001 # Frame wait time in seconds (30ms)
LED_COUNT      = SCREEN_COUNT_PRE + (SCREEN_COUNT_X * SCREEN_COUNT_Y) + SCREEN_COUNT_AFT  # Number of LED pixels.
LED_PIN        = 18      # GPIO pin connected to the pixels (18 uses PWM!).
#LED_PIN        = 10      # GPIO pin connected to the pixels (10 uses SPI /dev/spidev0.0).
LED_FREQ_HZ    = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA        = 10      # DMA channel to use for generating signal (try 10)
LED_BRIGHTNESS = 155     # Set to 0 for darkest and 255 for brightest
LED_INVERT     = False   # True to invert the signal (when using NPN transistor level shift)
LED_CHANNEL    = 0       # set to '1' for GPIOs 13, 19, 41, 45 or 53

# some colouring stuff from the original example.
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

# edited original example to use masks and run frame-by-frame.
j = 0
maxJ = 256
def rainbowCycle(strip, maskarray):
	"""Draw rainbow that uniformly distributes itself across all pixels, but just where the mask is set.
		ATTENTION: This function uses a FLAT mask!"""
	global j
	global maxJ
	for i in range(strip.numPixels()):
		# Here we check for the mask. i must be greater than the preled count and smaller than the screen end position.
		# Both are defined in the library file.
		if i>=SCREEN_COUNT_PRE and i<SCREEN_END_POSITION:
			maskpos = i-SCREEN_COUNT_PRE # mask position has no Pre-LED indexes so we subtract these.
			if maskpos>=0 and maskpos<len(maskarray):
				if maskarray[maskpos]!=0:				# colour only if the mask at this position is set.
					strip.setPixelColor(i,wheel((int(i*256/strip.numPixels())+j)&255))
	j=j-5	# adjust the colour "position".
	if j<=0:
		j=maxJ+j

###### RENDER FUNCTIONS ##########################

# clear all pixels
def clearScreen(strip, clearcolor):
	"""Clear all pixels on the screen."""
	for i in range(strip.numPixels()):
		strip.setPixelColor(i, clearcolor)
	strip.show()

# Render the background image.
actualPreLed = 0
actualPreLedColor = Color(0,0,255)
def renderBackground(strip):
	global actualPreLed
	global actualPreLedColor
	# just clear the screen. You could also do....other stuff here.
	clearScreen(strip, Color(0,0,0))
	# create some stuff for the wheel.
	strip.setPixelColor(actualPreLed,actualPreLedColor)
	actualPreLed=actualPreLed-1
	if actualPreLed<0:
		actualPreLed=11
	return 0

# some global variables for the foreground animation.
# I just learned python some days ago so please forgive me for not using classes or whatever...structs... :)
foregroundx=SCREEN_COUNT_X+1
oldtime= -1

# PART OF EXAMPLE: BUILD THE TEXT ARRAY
timearray = buildTextArray_x_6("0")
timearray = font_render

txt_width=0
def renderForeground(strip):
	# we will show the time in fancy rainbow colours here.
	global foregroundx
	global oldtime
	global txt_width
	global timearray

	# get the current time.
	currenttime = time.ctime(time.time())
	if(oldtime!=currenttime):
		# maybe build a new time array.
# PART OF EXAMPLE: BUILD THE TEXT ARRAY
#		timearray = buildTextArray_x_6(currenttime) # create the text array.
		oldtime = currenttime
		txt_width = len(timearray[0])
# BeLED EXAMPLE
	mask = createFlatScreenMask(timearray,foregroundx,0)
	rainbowCycle(strip, mask)
	foregroundx=foregroundx-1
	# reset text position
	if foregroundx <= -txt_width:
		foregroundx=SCREEN_COUNT_X+1
# Aaand done. :)
	return 0

# render a screenarray onto the strip.
#def renderArray(strip, screenarray, x, y):
	"""Render the screenarray onto the strip."""
"""
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
					strip.setPixelColor(pixelpos, col)"""

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
            clearScreen(strip, Color(0,0,0))
