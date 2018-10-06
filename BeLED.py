#!/usr/bin/env python3
# NeoPixel library strandtest example
# Author: Tony DiCola (tony@tonydicola.com)
#
# Direct port of the Arduino NeoPixel library strandtest example.  Showcases
# various animations on a strip of NeoPixels.

import time
from neopixel import *
import argparse

from BeFont_x_5 import getFontChar
font_render = getFontChar('Z')

# BeLED screen configuration
# The can have "lights" before and after it on the same line, for lighting other stuff also.
SCREEN_COUNT_PRE 	= 1		# Number of LEDs before the actual screen.
SCREEN_COUNT_X 		= 10	# Number of LEDs in one line on the screen.
SCREEN_COUNT_Y		= 10	# Number of lines on the screen.
SCREEN_COUNT_AFT	= 0		# Number of LEDs after the actual screen.

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

SCREEN_DIRECTION 	= 1     # 0 = normal, 1 = y flip, 2 = x flip, 3 = x & y flip

# render a screenarray on the strip.
def renderChar(strip, screenarray, x, y):
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
				col = Color(0,127,0)
				if setpix == 0:
					col = Color(0,0,0)
				if setpix == 1:
					col = Color(127,0,0)
				# set the color on the screen.	
				strip.setPixelColor(pixelpos, col)			
	strip.show();
	time.sleep(PIXELWAITTIME)

# clear all pixels
def clearScreen(strip):
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
			renderChar(strip,font_render,1,2)
           # print ('Color wipe animations.')
           # colorWipe(strip, Color(255, 0, 0))  # Red wipe
           # colorWipe(strip, Color(0, 255, 0))  # Blue wipe
           # colorWipe(strip, Color(0, 0, 255))  # Green wipe
           # print ('Theater chase animations.')
           # theaterChase(strip, Color(127, 127, 127))  # White theater chase
           # theaterChase(strip, Color(127,   0,   0))  # Red theater chase
           # theaterChase(strip, Color(  0,   0, 127))  # Blue theater chase
           # print ('Rainbow animations.')
           # rainbow(strip)
           # rainbowCycle(strip)
           # theaterChaseRainbow(strip)

    except KeyboardInterrupt:
        if args.clear:
            clearScreen(strip)