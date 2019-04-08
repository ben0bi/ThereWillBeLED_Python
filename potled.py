#!/usr/bin/env python3
# NeoPixel library strandtest example
# Author: Tony DiCola (tony@tonydicola.com)
#
# Direct port of the Arduino NeoPixel library strandtest example.  Showcases
# various animations on a strip of NeoPixels.

import time
from neopixel import *
import argparse

# lib needed for gpio input and output
import RPi.GPIO as GPIO

# New: Benobis stuff.
from BeLEDLib import *
from BeFont_x_6 import buildTextArray_x_6 as buildTextArray

# button pinouts
# ok is up, cancel is down. left is left and right is right.
GPIO_BTN_UP = 27
GPIO_BTN_DOWN = 17
GPIO_BTN_LEFT = 11
GPIO_BTN_RIGHT = 22

PRESSED = 0				# state of a button when it is pressed.
MENU_ON = 0				# is the menu on.

#benobi stuff.
show_text = 'Welcome to BeLED! @XOXO#'
show_text_array =  buildTextArray(show_text)
g_text_width = get2DTextArrayWidth(show_text_array)
g_posX = SCREEN_COUNT_X + 1

# characters to switch through.
g_actual_char = 0
g_char_array=['<SHOW>','a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u',
'v','w','x','y','z','.','=','+','-','*','0','1','2','3','4','5','6','7','8','9','[SPACE]','<OK>']

# initialize the GPIO buttons.
def initGPIO():
	# we use pull up and connect to GND! (5th pin)
	global GPIO_BTN_UP, GPIO_BTN_DOWN, GPIO_BTN_LEFT, GPIO_BTN_RIGHT
	GPIO.setmode(GPIO.BCM)
	GPIO.setup(GPIO_BTN_UP, GPIO.IN, pull_up_down = GPIO.PUD_UP)
	GPIO.setup(GPIO_BTN_DOWN, GPIO.IN, pull_up_down = GPIO.PUD_UP)
	GPIO.setup(GPIO_BTN_LEFT, GPIO.IN, pull_up_down = GPIO.PUD_UP)
	GPIO.setup(GPIO_BTN_RIGHT, GPIO.IN, pull_up_down = GPIO.PUD_UP)
	print ("GPIO setup done.")

# update the menu.
g_brp=0	#right button down?
g_blp=0 #left button down?
g_bdp=0 #down button down?
g_bup=0 #up button down?
def updateGPIO():
	global GPIO_BTN_UP, GPIO_BTN_DOWN, GPIO_BTN_LEFT, GPIO_BTN_RIGHT, PRESSED, MENU_ON
	global g_actual_char, g_char_array
	global show_text
	global g_brp, g_blp, g_bdp, g_bup
	
	bu = GPIO.input(GPIO_BTN_UP)
	bd = GPIO.input(GPIO_BTN_DOWN)
	bl = GPIO.input(GPIO_BTN_LEFT)
	br = GPIO.input(GPIO_BTN_RIGHT)
		
	if bu==PRESSED:
		print('UP pressed')
	if bd!=PRESSED:
		g_bdp=0
	if bl!=PRESSED:
		g_blp=0
	if br!=PRESSED:
		g_brp=0

# turn menu on.
	if bl==PRESSED and br==PRESSED and MENU_ON==0:
		print("MENU | <- previous char | -> next char | v add char | ^ delete char")
		print("TEXT> "+show_text)
		MENU_ON = 1

# change characters.
	if MENU_ON==1:
		#next char.
		changed = 0
		if br==PRESSED and g_brp!=1:
			g_actual_char = g_actual_char+1
			changed = 1
			g_brp=1
		#previous char.
		if bl == PRESSED and g_blp!=1:
			g_actual_char = g_actual_char-1
			changed = 1
			g_blp=1
		#constrain to array size.
		if g_actual_char < 0:
			g_actual_char = len(g_char_array)-1
		if g_actual_char >= len(g_char_array):
			g_actual_char=0
		
		#add the given character.
		if bd == PRESSED and g_bdp!=1:
			c = g_char_array[g_actual_char]
			if c == '[SPACE]':
				show_text = show_text+' '
			if c == '<OK>':
				MENU_ON = 0
			if c!='[SPACE]' and c!='<OK>' and c!='<SHOW>':
				show_text = show_text+g_char_array[g_actual_char]
			print('{'+show_text+'}')
			changed = 1
			g_bdp=1

		if changed == 1:
			print(g_char_array[g_actual_char])
		
# clean the GPIO status.
def cleanupGPIO():
	GPIO.cleanup()

PIXELWAITTIME = 40*0.001 # Frame wait time in seconds (30ms)

# clear all pixels
def clearScreen(strip, clearcolor):
	"""Clear all pixels on the screen."""
	for i in range(strip.numPixels()):
		strip.setPixelColor(i, clearcolor)

# PREDEFINED Functions. --------------------------------------------------------------------------------------------------------------------------------

# Define functions which animate LEDs in various ways.
def colorWipe(strip, color, wait_ms=50):
    """Wipe color across display a pixel at a time."""
    for i in range(strip.numPixels()):
        strip.setPixelColor(i, color)
        strip.show()
        time.sleep(wait_ms/1000.0)

def theaterChase(strip, color, wait_ms=50, iterations=10):
    """Movie theater light style chaser animation."""
    for j in range(iterations):
        for q in range(3):
            for i in range(0, strip.numPixels(), 3):
                strip.setPixelColor(i+q, color)
            strip.show()
            time.sleep(wait_ms/1000.0)
            for i in range(0, strip.numPixels(), 3):
                strip.setPixelColor(i+q, 0)

def wheel(pos):
    """Generate rainbow colors across 0-255 positions."""
    if pos < 85:
        return Color(pos * 3, 255 - pos * 3, 0)
    elif pos < 170:
        pos -= 85
        return Color(255 - pos * 3, 0, pos * 3)
    else:
        pos -= 170
        return Color(0, pos * 3, 255 - pos * 3)

def rainbow(strip, wait_ms=20, iterations=1):
    """Draw rainbow that fades across all pixels at once."""
    for j in range(256*iterations):
        for i in range(strip.numPixels()):
            strip.setPixelColor(i, wheel((i+j) & 255))
        strip.show()
        time.sleep(wait_ms/1000.0)

def rainbowCycle(strip, wait_ms=20, iterations=5):
    """Draw rainbow that uniformly distributes itself across all pixels."""
    for j in range(256*iterations):
        for i in range(strip.numPixels()):
            strip.setPixelColor(i, wheel((int(i * 256 / strip.numPixels()) + j) & 255))
        strip.show()
        time.sleep(wait_ms/1000.0)

def theaterChaseRainbow(strip, wait_ms=50):
    """Rainbow movie theater light style chaser animation."""
    for j in range(256):
        for q in range(3):
            for i in range(0, strip.numPixels(), 3):
                strip.setPixelColor(i+q, wheel((i+j) % 255))
            strip.show()
            time.sleep(wait_ms/1000.0)
            for i in range(0, strip.numPixels(), 3):
                strip.setPixelColor(i+q, 0)

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
            updateGPIO()
			
            # clear the screen with black.
            clearScreen(strip, Color(0,0,0))

			# finally show the strip and wait some time.
            strip.show()
            time.sleep(PIXELWAITTIME)
			
#            print ('Color wipe animations.')
#            colorWipe(strip, Color(255, 0, 0))  # Red wipe
#            colorWipe(strip, Color(0, 255, 0))  # Blue wipe
#            colorWipe(strip, Color(0, 0, 255))  # Green wipe
#            print ('Theater chase animations.')
#            theaterChase(strip, Color(127, 127, 127))  # White theater chase
#            theaterChase(strip, Color(127,   0,   0))  # Red theater chase
#            theaterChase(strip, Color(  0,   0, 127))  # Blue theater chase
#            print ('Rainbow animations.')
#            rainbow(strip)
#            rainbowCycle(strip)
#            theaterChaseRainbow(strip)

    except KeyboardInterrupt:
        if args.clear:
            colorWipe(strip, Color(0,0,0), 10)
        cleanupGPIO()
