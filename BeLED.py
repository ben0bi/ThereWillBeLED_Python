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

import RPi.GPIO as GPIO

from BeLEDLib import *

#from BeFont_x_6 import getCharArray_x_6
from BeFont_x_6 import buildTextArray_x_6
from BeSymbols_x_3 import buildSymbolArray_x_3

font_render = buildTextArray_x_6('III: Gaia    ') # This is the main x_6 font text, in rainbow colors.
symbol_render = buildSymbolArray_x_3('3')		  # This is the Symbol below the main text.

# The GPIO BCM numbers of the buttons to switch trough the menu items.
BCM_BTN_MAINMENU = 17		# Button number for the main menu
BCM_BTN_SUBMENU = 27		# Button number for the submenu
BCM_BTNPRESS_MAINMENU = 0	# Is the button already down?
BCM_BTNPRESS_SUBMENU = 0	# -"- ?

# Menu item stuff.
ACTUAL_MENU_ITEM = -1 	# Which menu is acutally on? Set to -1 for first first, else it is second first (at start of program)
ACTUAL_SUBMENU_ITEM = 0 # Same for the submenu.

# Menu Variables for display.
MENU_SHOW_TIME = 2.0	# How many seconds to show the menu entry?
MENU_CHANGED_TIME = 0.0	# Set the seconds to show the menu here.
# It will count down to 0 and then show the function.

# MAINMENU ITEMS:
# Name, Symbol
MAINMENU_ARRAY = [
["Time","0"],
["Date","1"],
["Calendar", "2"],
["Solar System","3"]
]

# initialize the GPIO buttons.
def initGPIO():
	global BCM_BTN_MAINMENU, BCM_BTN_SUBMENU
	GPIO.setmode(GPIO.BCM)
	GPIO.setup(BCM_BTN_MAINMENU, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)
	GPIO.setup(BCM_BTN_SUBMENU, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)
	print ("GPIO setup done.")

# update the GPIO buttons and switch through the menus.
def updateGPIOButtons():
	global BCM_BTN_MAINMENU, BCM_BTN_SUBMENU
	global BCM_BTNPRESS_MAINMENU, BCM_BTNPRESS_SUBMENU
	# get the buttons.
	btn_mm = GPIO.input(BCM_BTN_MAINMENU)
	btn_sm = GPIO.input(BCM_BTN_SUBMENU)
	# check them and do something.
	# check for the main menu.
	if btn_mm==1: # is the mainmenu button down?
		if BCM_BTNPRESS_MAINMENU == 0: # only do it once.
			advanceMenu(0)
		BCM_BTNPRESS_MAINMENU = 1 # set the button as pressed.
	else:
		BCM_BTNPRESS_MAINMENU = 0 # reset the button
	# same with the submenu.
	if btn_sm==1: # is the mainmenu button down?
		if BCM_BTNPRESS_SUBMENU == 0: # only do it once.
			advanceMenu(1)
		BCM_BTNPRESS_SUBMENU = 1 # set the button as pressed.
	else:
		BCM_BTNPRESS_SUBMENU = 0 # reset the button

# advance the menu.
def advanceMenu(isSubMenu):
	global ACTUAL_MENU_ITEM, ACTUAL_SUBMENU_ITEM
	global MAINMENU_ARRAY
	global MENU_CHANGED_TIME, MENU_SHOW_TIME
	global symbol_render, symbol_width
	
	if isSubMenu == 0:
		ACTUAL_SUBMENU_ITEM = 0 # Reset the actual submenu item.
		ACTUAL_MENU_ITEM = ACTUAL_MENU_ITEM + 1
		if ACTUAL_MENU_ITEM >= len(MAINMENU_ARRAY):
			ACTUAL_MENU_ITEM = 0
	else:
		ACTUAL_SUBMENU_ITEM = ACTUAL_SUBMENU_ITEM + 1

	# create the symbol for the menu.
	symbol_render = buildSymbolArray_x_3(MAINMENU_ARRAY[ACTUAL_MENU_ITEM][1]) # This is the Symbol below the main text.
	symbol_width = len(symbol_render[0])
	
	MENU_CHANGED_TIME = MENU_SHOW_TIME		
	print("Menu selection: "+str(ACTUAL_MENU_ITEM)+" Submenu: "+str(ACTUAL_SUBMENU_ITEM))

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

# New: Palette
# Use the values 1 through 9 in your symbols, and then use renderPalette(mask,paleteIndex)
BeLED_Palette=[
Color(0,0,0),			# If it is not transparent, 0 is black.
Color(255,255,127),
Color(255,255,0),
Color(127,255,0),
Color(0,255,0),
Color(0,255,255),
Color(0,127,255),
Color(0,0,255),
Color(255,0,255),
Color(255,0,0)
]

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
	for i in range(SCREEN_COUNT_PRE,SCREEN_END_POSITION):
		# Here we check for the mask. i must be greater than the preled count and smaller than the screen end position.
		# Both are defined in the library file.
		if i>=SCREEN_COUNT_PRE and i<SCREEN_END_POSITION:
			maskpos = i-SCREEN_COUNT_PRE # mask position has no Pre-LED indexes so we subtract these.
			if maskpos>=0 and maskpos<len(maskarray):
				if maskarray[maskpos]!=0: # colour only if the mask at this position is set.
					strip.setPixelColor(i,wheel((int(i*256/strip.numPixels())+j)&255))
	j=j-5	# adjust the colour "position".
	if j<=0:
		j=maxJ+j
		
def renderPaletteTransparent(strip, maskarray):
	"""Draw a mask with the palette colours for their corresponding numbers.
		ATTENTION: This function usses a FLAT mask.
		0 values will NOT be blacked out."""
	for i in range(SCREEN_COUNT_PRE,SCREEN_END_POSITION):
		# Here we check for the mask. i must be greater than the preled count and smaller than the screen end position.
		# Both are defined in the library file.
		if i>=SCREEN_COUNT_PRE and i<SCREEN_END_POSITION:
			maskpos = i-SCREEN_COUNT_PRE # mask position has no Pre-LED indexes so we subtract these.
			if maskpos>=0 and maskpos<len(maskarray):
				m = maskarray[maskpos]
				if m!=0: # colour only if the mask at this position is set.
					col = BeLED_Palette[m]
					strip.setPixelColor(i,col)

###### RENDER FUNCTIONS ##########################

# clear all pixels
def clearScreen(strip, clearcolor):
	"""Clear all pixels on the screen."""
	for i in range(strip.numPixels()):
		strip.setPixelColor(i, clearcolor)
	
# get the text widths for floating.
txt_width=len(font_render[0])
foregroundx=SCREEN_COUNT_X+1

symbol_width = len(symbol_render[0])
symbolx = -symbol_width

# render the menu.
def renderMenu(strip):
	global ACTUAL_MENU_ITEM
	global MAINMENU_ARRAY
	global symbol_render

	m = ACTUAL_MENU_ITEM
	max = len(MAINMENU_ARRAY)
	
	menucolor = Color(126,255,0)
	bordercolor = Color(0,255,0)
	# maybe draw a border.
	if max<12:
		# advance the LED by one.
		m = ACTUAL_MENU_ITEM+1
		# light up the first "left" border.
		strip.setPixelColor(0,bordercolor)
		if max<11:
			strip.setPixelColor(max+1, bordercolor)

	# show the menu indicator.
	if ACTUAL_MENU_ITEM >= 0 and ACTUAL_MENU_ITEM < SCREEN_COUNT_PRE:
		strip.setPixelColor(m, menucolor)

	# create the mask with the symbol and draw it.
	symask = createFlatScreenMask(symbol_render, 0, 6)
	renderPaletteTransparent(strip,symask)
		
# Render the background image.
actualPreLed = 0
actualPreLedColor = Color(0,0,255)
def renderBackground(strip):
	global actualPreLed
	global actualPreLedColor
	# create some stuff for the wheel.
	strip.setPixelColor(actualPreLed,actualPreLedColor)
	actualPreLed=actualPreLed-1
	if actualPreLed<0:
		actualPreLed=11
	return 0

# PART OF EXAMPLE: BUILD THE TEXT ARRAY

def renderForeground(strip):
	# we will show the time in fancy rainbow colours here.
	global foregroundx
	global symbolx
	#global oldtime
	global symbol_width
	global txt_width
	global font_render
	global symbol_render

	# get the current time.
	#currenttime = time.ctime(time.time())
	#if(oldtime!=currenttime):
		# maybe build a new time array.
# PART OF EXAMPLE: BUILD THE TEXT ARRAY
#		timearray = buildTextArray_x_6(currenttime) # create the text array.
		#oldtime = currenttime
		#txt_width = len(timearray[0])
# BeLED EXAMPLE
	# create the mask for the upper text.
	mask = createFlatScreenMask(font_render,foregroundx,0)
	# create the mask for the lower symbol text.
	mask2 = createFlatScreenMask(symbol_render, 0, 6)
	# combine the masks.
	#combinedmask = combineFlatScreenMasks_OR(mask,mask2)
	
	# rainbow the masks on the strip, du weisch scho, s rägeboge chotzende internetz-einhorn :)
	rainbowCycle(strip, mask)
	renderPaletteTransparent(strip,mask2)
	
	# set/reset text position
	foregroundx=foregroundx-1
	if foregroundx <= -txt_width:
		foregroundx=SCREEN_COUNT_X+1
		
	# set/reset symbol position.
	symbolx=symbolx+1
	if symbolx > SCREEN_COUNT_X:
		symbolx = -symbol_width

# Aaand done. :)
	return 0

# Main program logic follows:
if __name__ == '__main__':
    # Process arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--clear', action='store_true', help='clear the display on exit')
    args = parser.parse_args()
    initGPIO()
	
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
			updateGPIOButtons()
			# clear the screen with black.
			clearScreen(strip, Color(0,0,0))
			if(MENU_CHANGED_TIME > 0.0):
				renderMenu(strip)
				MENU_CHANGED_TIME = MENU_CHANGED_TIME - PIXELWAITTIME
			else:
				renderBackground(strip)
				renderForeground(strip)

			if(MENU_CHANGED_TIME<0.0):
				MENU_CHANGED_TIME = 0
				
			# finally show the strip and wait some time.
			strip.show()
			time.sleep(PIXELWAITTIME)

    except KeyboardInterrupt:
        if args.clear:
            clearScreen(strip, Color(0,0,0))
            strip.show()
            GPIO.cleanup()