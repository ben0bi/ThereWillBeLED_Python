#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# FONT to be used with BeLED.py
# BeSymbols: Some symbols in height 3, like CAL for Calendar, DAT for Date, etc.
# Ben0bi fonts are determined by their size.
# by oki wan ben0bi @ 2018
# Font consists of char arrays.
# a char array has a specific amount of lines with variable line length.
# The line length must match each line in the same char array.
# The line count must match each char in the font array.

# return the char array for a given character.
# returns -1 the character is part of a special character.
symbols_x_3_prechar = ''
def getSymbolArray_x_3(character):
	"""Returns the char array associated to the given character."""
	global symbols_x_3_prechar
	# is it a special character prefix?
	if ord(character)==195:
		# then set the prefix and return -1
		symbols_x_3_prechar=chr(195)
		return -1
	else:
		# add the character. maybe add the special character prefix (again) to the character.
		ch = symbols_x_3_prechar + character
		symbols_x_3_prechar = '' # reset the prefix character to nothing.
		if ch in symbols_x_3_FIDX:
			c = symbols_x_3_FIDX.index(ch)
			if c>=0 and c<len(symbols_x_3_FONT):
				return symbols_x_3_FONT[c]
		# the character is not in the list.
		print("Character not found: "+character+"("+str(ord(character))+")")
		return symbols_x_3_font_notfound

# build a text line screenarray
def buildSymbolArray_x_3(text):
	"""Build a text array from a given text."""
	txtarr = []
	# create the lines
	for i in range(6):
		txtarr.append([])
	# go through each character in the text and add the character to the array.
	for c in text:
		charr = getSymbolArray_x_3(c)
		if charr!=-1:
			for y in range(len(charr)):
				for x in range(len(charr[y])):
					txtarr[y].append(charr[y][x])
	return txtarr

# Now follows each char in the font.
# It will be assembled into the x_6_FONT and x_6_FIDX arrays at the bottom of the file.

# This one will be returned directly.
symbols_x_3_font_notfound = [
[0,0,0,0],
[0,1,0,0],
[0,0,0,0]
]

# These characters will be added to the FONT array.

# Time Symbols
font_CAL = [
[1,1,0,0,1,1,0,1,0,0],
[1,0,0,1,0,1,0,1,0,0],
[1,1,0,1,1,1,0,1,1,0]
]

font_TIM = [
[1,1,1,0,1,0,1,1,1,1,1,0],
[0,1,0,0,1,0,1,0,1,0,1,0],
[0,1,0,0,1,0,1,0,0,0,1,0]
]

font_DAT = [
[1,1,0,0,0,1,1,0,1,1,1,0],
[1,0,1,0,1,0,1,0,0,1,0,0],
[1,1,0,0,1,1,1,0,0,1,0,0]
]

font_PALETTE = [
[1,2,3,4,5,6,7,8,9,0],
[1,2,3,4,5,6,7,8,9,0],
[1,2,3,4,5,6,7,8,9,0]
]

font_SOLSYS = [
[0,2,0,0,0,0,0,0,0,0,0,0],
[2,2,2,0,2,0,1,0,8,0,4,0],
[0,2,0,0,0,0,0,0,0,0,0,0]
]

font_SOLSYS = [
[0,2,0,0,0,0,0,0,0,0],
[2,2,2,0,1,0,7,0,4,0],
[0,2,0,0,0,0,0,0,0,0]
]

font_SPACE = [
[0,0,0],
[0,0,0],
[0,0,0]
]

# FIDX represents all the indexes in the FONT array. get a character (here: A) like this: charpixels = FONT[FIDX.index('A')]
# The characters in FIDX MUST have the same order as they are added to the FONT array.
symbols_x_3_FIDX=[]
symbols_x_3_FIDX.extend(('P',' ','0','1','2','3'))

# The real character arrays are in the FONT array.
symbols_x_3_FONT=[]
symbols_x_3_FONT.extend((font_PALETTE, font_SPACE, font_CAL,font_TIM,font_DAT,font_SOLSYS))
