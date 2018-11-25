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
import BeGPIOMenu as MENU

#from BeFont_x_6 import getCharArray_x_6
from BeFont_x_6 import buildTextArray_x_6
from BeSymbols_x_4 import buildSymbolArray_x_4

# save the submenu in the lights function,
# to get it back when the main function changes.
ACTUAL_LIGHT_ITEM = 0

# how many repeats of the welcome screen?
SHOW_WELCOME_SCREEN_REPEATS = 3

font_render = buildTextArray_x_6('Welcome to BeLED!') 	# This is the main x_6 font text, in rainbow colors.
symbol_render = buildSymbolArray_x_4('3')		  		# This is the Symbol below the main text.
g_symbolmask = createFlatScreenMask(symbol_render,0,5)	# the mask for the symbol is global because it does not move.

# get the text widths for floating.
g_textWidth=len(font_render[0])
g_textX=SCREEN_COUNT_X+1

# time variables
g_oldtime = ""

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
		ATTENTION: This function uses a FLAT mask.
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

def renderSingleColorTransparent(strip,maskarray,rendercolor):
	"""Draw a mask with the given colour for each number > 0.
		ATTENTION: This function uses a FLAT mask.
		0 values will NOT be blacked out."""
	for i in range(SCREEN_COUNT_PRE,SCREEN_END_POSITION):
		# Here we check for the mask. i must be greater than the preled count and smaller than the screen end position.
		# Both are defined in the library file.
		if i>=SCREEN_COUNT_PRE and i<SCREEN_END_POSITION:
			maskpos = i-SCREEN_COUNT_PRE # mask position has no Pre-LED indexes so we subtract these.
			if maskpos>=0 and maskpos<len(maskarray):
				m = maskarray[maskpos]
				if m>0: # colour only if the mask at this position is set.
					col = BeLED_Palette[m]
					strip.setPixelColor(i,rendercolor)

# update the text x.
def updateTextX():
	global g_textX, g_textWidth, SCREEN_COUNT_X
	g_textX = g_textX - 1
	if g_textX < -g_textWidth:
		g_textX = SCREEN_COUNT_X + 1

# set a new text and text x.		
def setRenderText(txt):
	global g_textX, g_textWidth
	global font_render
	global SCREEN_COUNT_X
	
	g_textX = SCREEN_COUNT_X+1
	font_render = buildTextArray_x_6(txt)
	g_textWidth = len(font_render[0])
	
###### RENDER FUNCTIONS ##########################

# clear all pixels
def clearScreen(strip, clearcolor):
	"""Clear all pixels on the screen."""
	for i in range(strip.numPixels()):
		strip.setPixelColor(i, clearcolor)

# render the menu.
def renderMenu(strip):
	global symbol_render
	global g_textX, font_render
	
	itm = MENU.getActualMenuItem()
	m = itm
	max = MENU.getMainMenuCount()
	
	menucolor = Color(126,255,0)
	bordercolor = Color(0,255,0)
	# maybe draw a border.
	if max<12:
		# advance the LED by one.
		m = itm+1
		# light up the first "left" border.
		strip.setPixelColor(0,bordercolor)
		if max<11:
			strip.setPixelColor(max+1, bordercolor)

	# show the menu indicator.
	if m >= 0 and m < SCREEN_COUNT_PRE:
		strip.setPixelColor(m, menucolor)

	# draw the mask with the symbol.
	symask = createFlatScreenMask(symbol_render, 0, 5)
	renderPaletteTransparent(strip,symask)

	# draw the menu text.
	txtmask = createFlatScreenMask(font_render,g_textX,0)	
	rainbowCycle(strip, txtmask)
	
	updateTextX()
	

# render the stuff for the actual function.
LIGHTCONE_FLATMASK = [
0,0,0,0,0,0,0,0,0,0,
0,0,0,3,3,3,3,0,0,0,
0,0,3,3,2,2,3,3,0,0,
0,3,3,2,2,2,2,3,3,0,
0,3,2,2,1,1,2,2,3,0,
0,3,2,2,1,1,2,2,3,0,
0,3,3,2,2,2,2,3,3,0,
0,0,3,3,2,2,3,3,0,0,
0,0,0,3,3,3,3,0,0,0,
0,0,0,0,0,0,0,0,0,0,
]

oldTimeSubmenu = -1
smoothSeconds = 0.0
oldTsmod = -1

# This function renders the time.
def renderTimeFunction(strip):
	"Render actual time and date."
	global g_oldtime
	global g_textWidth, g_textX, g_fontmask
	global font_render, symbol_render, g_symbolmask
	global oldTimeSubmenu
	global smoothSeconds, oldTsmod, PIXELWAITTIME
		
	maxTimeMenus = 3 # how many submenus has this function?
		
	# 1 time with text
	# 2 date with text
	# 3 time only on wheel
		
	s=MENU.getActualSubmenuItem()
	#create the symbols
	if oldTimeSubmenu!=s:
		oldTimeSubmenu=s
		if s==0:	# show time
			symbol_render=buildSymbolArray_x_4('T')
		if s==1:	# show date
			symbol_render=buildSymbolArray_x_4('D')
		if s==2 or s==3:	# show only clock without anything other.
			symbol_render = buildSymbolArray_x_4(' ')		
		g_symbolmask = createFlatScreenMask(symbol_render, 0,5)
		
	# get the current time.
#		currenttime = time.ctime(time.time())
	current_time = time.localtime()

	# maybe reset submenu
	if s>=maxTimeMenus:
		MENU.setActualSubmenuItem(0)
		s=0

	# show time or date (text)
	tt=""
	if s==0:
		tt=time.strftime('%H:%M', current_time)
	# show date
	if s==1:
		tt=time.strftime('%d.%B %Y', current_time)
	if s==2 or s==3: # show only time on wheel.
		tt=" "

	# maybe reset the text
	if(g_oldtime!=tt):
		font_render = buildTextArray_x_6(tt) # create the text array.
		g_oldtime = tt
		g_textWidth = len(font_render[0])	

	# set text x.
	updateTextX()
		
	# render text to strip.
	mask = createFlatScreenMask(font_render, g_textX, 0)
	rainbowCycle(strip, mask)
	renderPaletteTransparent(strip, g_symbolmask)
			
	# show time on wheel
	# colors corresponding to the symbol colors (font_TIME)
	if s==0 or s==2 or s==3:
		th=int(time.strftime('%I', current_time)) 	# get hour (1-12)
		tm=int(time.strftime('%M',current_time))	# get minute (1-60)
		tsec=int(time.strftime('%S',current_time))	# get second (1-60)
		tsmod = 0 # tsmod is the amount of light for the actual and the next LED.
			
		# set 12 to the first LED (0)
		if th >= 12:
			th = 0 
			
		# normalize the minutes.
		if tm > 0:
			tm=int((12.0/60.0)*tm)
			if tm>=12:
				tm=0
		
		# normalize the seconds.
		if tsec > 0:
			tsmod=tsec%5 # amount of light on the LEDs
			tsec=int((12.0/60.0)*tsec)
			if tsec >= 12:
				tsec=0

		#tsec2 is the second LED for the seconds.
		tsec2=tsec+1
		if tsec2>=12:
			tsec2=tsec2-12

		# maybe reset the smooth seconds.
		if oldTsmod!=tsmod:
			oldTsmod = tsmod
			smoothSeconds = 0.0
			
		# create the colouring.
		up=int((255.0/6 * tsmod)+(255.0/6*smoothSeconds))
		down=int(255.0/6 * (6-tsmod)-(255.0/6*smoothSeconds))
			
		smoothSeconds = smoothSeconds + PIXELWAITTIME
		if smoothSeconds>1.0:
			smoothSeconds = 1.0
			
		c1 = Color(0,down,0)
		c2 = Color(0,up,0)
		clockcol = BeLED_Palette[3]
		minutecol = BeLED_Palette[7]
		strip.setPixelColor(tsec,c1)
		strip.setPixelColor(tsec2,c2)
		strip.setPixelColor(tm,minutecol)
		strip.setPixelColor(th,clockcol)

def renderLightFunction(strip):
	"Render just some lights."
	global LIGHTCONE_FLATMASK			# the mask for the lighting, so it appears round.
	global SCREEN_COUNT_PRE
	global ACTUAL_LIGHT_ITEM
	
	s=MENU.getActualSubmenuItem()
	if s>=29: # 29 light modes, yay
		MENU.setActualSubmenuItem(0)
		s=0
	ACTUAL_LIGHT_ITEM = s

	# get the palette color.
	pc = (s-2)%9
	palettecol = BeLED_Palette[pc+1] # palette 0 = black

	# original light cone light.
	if s < 2:
		renderPaletteTransparent(strip,LIGHTCONE_FLATMASK)
		palettecol=BeLED_Palette[3]

	# draw outer circle
	if s < 20 and s!=1:
		for i in range(SCREEN_COUNT_PRE):
			strip.setPixelColor(i,palettecol)

	# draw inner circle
	if (s>=2 and s<=10) or s>=20:
		renderSingleColorTransparent(strip,LIGHTCONE_FLATMASK,palettecol)
		
def renderFunction(strip):
	"Render something."
	global SHOW_WELCOME_SCREEN_REPEATS	# how many repeats of the welcome screen?
	global SCREEN_COUNT_X
	global g_textX, g_textWidth
	global font_render

	if SHOW_WELCOME_SCREEN_REPEATS>0:
		#SHOW_WELCOME_SCREEN_TIME = SHOW_WELCOME_SCREEN_TIME-PIXELWAITTIME
		mask = createFlatScreenMask(font_render,g_textX,2)
		g_textX = g_textX-1
		if g_textX < -g_textWidth:
			g_textX = SCREEN_COUNT_X+1
			SHOW_WELCOME_SCREEN_REPEATS=SHOW_WELCOME_SCREEN_REPEATS-1
		rainbowCycle(strip, mask)
		return

	# get the actual function to draw.
	func = MENU.getActualMenuItemFunction()

	# show nothing.
	if func=="off":
		# todo: maybe show next calendar entry here.
		return 0

	# just some lights.
	if func=="light":
		renderLightFunction(strip)

	# show actual time and date.
	if func=="clock":
		renderTimeFunction(strip)

# Aaand done. :)
	return 0

# Main program logic follows:
if __name__ == '__main__':
	# Process arguments
	parser = argparse.ArgumentParser()
	parser.add_argument('-c', '--clear', action='store_true', help='clear the display on exit')
	args = parser.parse_args()

	# initialize the menu GPIO stuff.
	MENU.initGPIO()

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
			MENU.updateGPIOButtons()

			# the main menu changed, get the right symbol and stuff.
			if MENU.menuHasChanged() > 0:
				# create the symbol for the menu.
				symbol_render = buildSymbolArray_x_4(MENU.MAINMENU_ARRAY[MENU.ACTUAL_MENU_ITEM][1]) # This is the Symbol below the main text.
				symbol_width = len(symbol_render[0])
				setRenderText(MENU.MAINMENU_ARRAY[MENU.ACTUAL_MENU_ITEM][0])
				# stop the welcome screen when menu changed.
				SHOW_WELCOME_SCREEN_REPEATS = 0
				# get the actual function to draw.
				func = MENU.getActualMenuItemFunction()
				# set submenu parameters
				if func == "light":
					MENU.setActualSubmenuItem(ACTUAL_LIGHT_ITEM)

			# clear the screen with black.
			clearScreen(strip, Color(0,0,0))

			# show menu or function.
			if(MENU.getMenuChangeTime() > 0.0):
				renderMenu(strip)
			else:
				renderFunction(strip)

			# finally show the strip and wait some time.
			strip.show()
			MENU.updateMenuChangeTime(PIXELWAITTIME)
			time.sleep(PIXELWAITTIME)

	except KeyboardInterrupt:
		if args.clear:
			clearScreen(strip, Color(0,0,0))
			strip.show()
			MENU.cleanupGPIO()
