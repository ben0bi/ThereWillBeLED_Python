#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# FONT to be used with BeLED.py
# BeFont_x_5: Chars have the size of X*5 pixels.
# Ben0bi fonts are determined by their size.
# by oki wan ben0bi @ 2018
# Font consists of char arrays.
# a char array has a specific amount of lines with variable line length.
# The line length must match each line in the same char array.
# The line count must match each char in the font array.

# return the char array for a given character.
# returns -1 the character is part of a special character.
x_5_prechar = ''
def getCharArray_x_5(character):
	"""Returns the char array associated to the given character."""
	global x_5_prechar
	# is it a special character prefix?
	if ord(character)==195:
		# then set the prefix and return -1
		x_5_prechar=chr(195)
		return -1
	else:
		# add the character. maybe add the special character prefix (again) to the character.
		ch = x_5_prechar + character
		x_5_prechar = '' # reset the prefix character to nothing.
		if ch in x_5_FIDX:
			c = x_5_FIDX.index(ch)
			if c>=0 and c<len(x_5_FONT):
				return x_5_FONT[c]
		# the character is not in the list.
		print("Character not found: "+character+"("+str(ord(character))+")")
		return x_5_font_notfound

# build a text line screenarray
def buildTextArray_x_5(text):
	"""Build a text array from a given text."""
	txtline = []
	# create the lines
	for i in range(5):
		txtline.append([])
	# go through each character in the text and add the character to the array.
	for c in text:
		charr = getCharArray_x_5(c)
		if charr!=-1:
			for y in range(len(charr)):
				for x in range(len(charr[y])):
					txtline[y].append(charr[y][x])
	return txtline

# Now follows each char in the font.
# It will be assembled into the x_5_FONT and x_5_FIDX array at the bottom of the file.

# This one will be returned directly.
x_5_font_notfound = [
[1,1,1,1,1,0],
[1,1,0,1,1,0],
[1,0,1,0,1,0],
[1,1,0,1,1,0],
[1,1,1,1,1,0]
]

# These characters will be added to the FONT array.

# Numbers
font_0 = [
[0,1,1,1,0,0],
[1,0,0,1,1,0],
[1,0,1,0,1,0],
[1,1,0,0,1,0],
[0,1,1,1,0,0]
]

font_1 = [
[0,1,0],
[1,1,0],
[0,1,0],
[0,1,0],
[0,1,0]
]

font_2 = [
[0,1,1,0,0],
[1,0,0,1,0],
[0,0,1,0,0],
[0,1,0,0,0],
[1,1,1,1,0]
]

font_3 = [
[1,1,1,0,0],
[0,0,0,1,0],
[0,1,1,0,0],
[0,0,0,1,0],
[1,1,1,0,0]
]

font_4 = [
[0,0,0,1,0,0],
[0,0,1,1,0,0],
[0,1,0,1,0,0],
[1,1,1,1,1,0],
[0,0,0,1,0,0]
]

font_5 = [
[1,1,1,1,0],
[1,0,0,0,0],
[1,1,1,0,0],
[0,0,0,1,0],
[1,1,1,0,0]
]

font_6 = [
[0,1,1,0,0],
[1,0,0,0,0],
[1,1,1,0,0],
[1,0,0,1,0],
[0,1,1,0,0]
]

font_7 = [
[1,1,1,1,0],
[0,0,0,1,0],
[0,0,1,0,0],
[0,1,0,0,0],
[0,1,0,0,0]
]

font_8 = [
[0,1,1,0,0],
[1,0,0,1,0],
[0,1,1,0,0],
[1,0,0,1,0],
[0,1,1,0,0]
]

font_9 = [
[0,1,1,0,0],
[1,0,0,1,0],
[0,1,1,1,0],
[0,0,0,1,0],
[0,1,1,0,0]
]

# BIG characters
font_Ab = [
[0,1,1,0,0],
[1,0,0,1,0],
[1,1,1,1,0],
[1,0,0,1,0],
[1,0,0,1,0]
]

font_AEb = [
[1,0,0,1,0],
[0,1,1,0,0],
[1,0,0,1,0],
[1,1,1,1,0],
[1,0,0,1,0]
]

font_Bb = [
[1,1,1,0,0],
[1,0,0,1,0],
[1,1,1,0,0],
[1,0,0,1,0],
[1,1,1,0,0]
]

font_Cb = [
[0,1,1,0],
[1,0,0,0],
[1,0,0,0],
[1,0,0,0],
[0,1,1,0]
]

font_Db = [
[1,1,1,0,0],
[1,0,0,1,0],
[1,0,0,1,0],
[1,0,0,1,0],
[1,1,1,0,0]
]

font_Eb = [
[1,1,1,0],
[1,0,0,0],
[1,1,0,0],
[1,0,0,0],
[1,1,1,0]
]

font_Fb = [
[1,1,1,0],
[1,0,0,0],
[1,1,0,0],
[1,0,0,0],
[1,0,0,0]
]

font_Gb = [
[0,1,1,1,0],
[1,0,0,0,0],
[1,0,1,1,0],
[1,0,0,1,0],
[0,1,1,0,0]
]

font_Hb = [
[1,0,0,1,0],
[1,0,0,1,0],
[1,1,1,1,0],
[1,0,0,1,0],
[1,0,0,1,0]
]

font_Ib = [
[1,1,1,0],
[0,1,0,0],
[0,1,0,0],
[0,1,0,0],
[1,1,1,0]
]

font_Jb = [
[1,1,1,1,0],
[0,0,0,1,0],
[0,0,0,1,0],
[1,0,0,1,0],
[0,1,1,0,0]
]

font_Kb = [
[1,0,0,1,0],
[1,0,1,0,0],
[1,1,0,0,0],
[1,0,1,0,0],
[1,0,0,1,0]
]

font_Lb = [
[1,0,0,0],
[1,0,0,0],
[1,0,0,0],
[1,0,0,0],
[1,1,1,0]
]

font_Mb = [
[1,0,0,0,1,0],
[1,1,0,1,1,0],
[1,0,1,0,1,0],
[1,0,0,0,1,0],
[1,0,0,0,1,0]
]

font_Nb = [
[1,0,0,0,1,0],
[1,1,0,0,1,0],
[1,0,1,0,1,0],
[1,0,0,1,1,0],
[1,0,0,0,1,0]
]

font_Ob = [
[0,1,1,0,0],
[1,0,0,1,0],
[1,0,0,1,0],
[1,0,0,1,0],
[0,1,1,0,0]
]

font_OEb = [
[1,0,0,1,0],
[0,1,1,0,0],
[1,0,0,1,0],
[1,0,0,1,0],
[0,1,1,0,0]
]

font_Pb = [
[1,1,1,0,0],
[1,0,0,1,0],
[1,1,1,0,0],
[1,0,0,0,0],
[1,0,0,0,0]
]

font_Qb = [
[0,1,1,0,0,0],
[1,0,0,1,0,0],
[1,0,0,1,0,0],
[1,0,1,1,0,0],
[0,1,1,1,1,0]
]

font_Rb = [
[1,1,1,0,0],
[1,0,0,1,0],
[1,1,1,0,0],
[1,0,1,0,0],
[1,0,0,1,0]
]

font_Sb = [
[0,1,1,1,0],
[1,0,0,0,0],
[0,1,1,0,0],
[0,0,0,1,0],
[1,1,1,0,0]
]

font_Tb = [
[1,1,1,1,1,0],
[0,0,1,0,0,0],
[0,0,1,0,0,0],
[0,0,1,0,0,0],
[0,0,1,0,0,0]
]

font_Ub = [
[1,0,0,0,1,0],
[1,0,0,0,1,0],
[1,0,0,0,1,0],
[1,0,0,0,1,0],
[0,1,1,1,0,0]
]

font_UEb = [
[0,1,0,1,0,0],
[1,0,0,0,1,0],
[1,0,0,0,1,0],
[1,0,0,0,1,0],
[0,1,1,1,0,0]
]

font_Vb = [
[1,0,0,0,1,0],
[1,0,0,0,1,0],
[0,1,0,1,0,0],
[0,1,0,1,0,0],
[0,0,1,0,0,0]
]

font_Wb = [
[1,0,0,0,0,0,1,0],
[1,0,0,0,0,0,1,0],
[0,1,0,1,0,1,0,0],
[0,1,0,1,0,1,0,0],
[0,0,1,0,1,0,0,0]
]

font_Xb = [
[1,0,0,0,1,0],
[0,1,0,1,0,0],
[0,0,1,0,0,0],
[0,1,0,1,0,0],
[1,0,0,0,1,0]
]

font_Yb = [
[1,0,0,0,1,0],
[0,1,0,1,0,0],
[0,0,1,0,0,0],
[0,0,1,0,0,0],
[0,0,1,0,0,0]
]

font_Zb = [
[1,1,1,1,1,0],
[0,0,0,1,0,0],
[0,0,1,0,0,0],
[0,1,0,0,0,0],
[1,1,1,1,1,0]
]

# Special characters (dots, lines, etc.)
font_SPACE = [
[0,0,0,0,0],
[0,0,0,0,0],
[0,0,0,0,0],
[0,0,0,0,0],
[0,0,0,0,0]
]

font_DOT = [
[0,0,0,0,0],
[0,0,0,0,0],
[0,0,0,0,0],
[0,0,0,0,0],
[1,0,0,0,0]
]

font_COMMA = [
[0,0,0,0,0],
[0,0,0,0,0],
[0,0,0,0,0],
[0,1,0,0,0],
[1,0,0,0,0]
]

font_DBLDOT = [
[0,0,0,0,0],
[1,0,0,0,0],
[0,0,0,0,0],
[0,0,0,0,0],
[1,0,0,0,0]
]

font_DBLCOMMA = [
[0,0,0,0,0],
[0,1,0,0,0],
[0,0,0,0,0],
[0,1,0,0,0],
[1,0,0,0,0]
]

font_QUESTION = [
[1,1,0,0],
[0,0,1,0],
[0,1,0,0],
[0,0,0,0],
[0,1,0,0]
]

font_EXCLAMATION = [
[1,0,0,0,0],
[1,0,0,0,0],
[1,0,0,0,0],
[0,0,0,0,0],
[1,0,0,0,0]
]

font_PLUS = [
[0,0,0,0],
[0,1,0,0],
[1,1,1,0],
[0,1,0,0],
[0,0,0,0]
]

font_MINUS = [
[0,0,0,0],
[0,0,0,0],
[1,1,1,0],
[0,0,0,0],
[0,0,0,0]
]

font_SLASH = [
[0,0,1,0],
[0,0,1,0],
[0,1,0,0],
[1,0,0,0],
[1,0,0,0]
]

font_BACKSLASH = [
[1,0,0,0],
[1,0,0,0],
[0,1,0,0],
[0,0,1,0],
[0,0,1,0]
]

font_BRACEOPEN = [
[0,1,0],
[1,0,0],
[1,0,0],
[1,0,0],
[0,1,0]
]

font_BRACECLOSE = [
[1,0,0],
[0,1,0],
[0,1,0],
[0,1,0],
[1,0,0]
]

font_AT = [
[0,1,1,1,0],
[1,0,0,0,1],
[1,0,1,0,1],
[1,1,0,1,1],
[0,1,1,0,1]
]

font_HASHTAG = [
[0,1,0,1,0],
[1,1,1,1,1],
[0,1,0,1,0],
[1,1,1,1,1],
[0,1,0,1,0]
]

font_UNDERLINE = [
[0,0,0,0,0],
[0,0,0,0,0],
[0,0,0,0,0],
[0,0,0,0,0],
[1,1,1,1,0]
]

font_EQUAL = [
[0,0,0,0,0],
[1,1,1,1,0],
[0,0,0,0,0],
[1,1,1,1,0],
[0,0,0,0,0]
]

font_TIMES = [
[0,0,0,0],
[1,0,1,0],
[0,1,0,0],
[1,0,1,0],
[0,0,0,0]
]

font_PERCENT = [
[1,1,0,0,1,0],
[1,1,0,1,0,0],
[0,0,1,0,0,0],
[0,1,0,1,1,0],
[1,0,0,1,1,0]
]

font_GREATER = [
[1,0,0,0],
[0,1,0,0],
[0,0,1,0],
[0,1,0,0],
[1,0,0,0]
]

font_LESSER = [
[0,0,1,0],
[0,1,0,0],
[1,0,0,0],
[0,1,0,0],
[0,0,1,0]
]

# FIDX represents all the indexes in the FONT array. get a character (here: A) like this: charpixels = FONT[FIDX.index('A')]
# The characters in FIDX MUST have the same order as they are added to the FONT array.
x_5_FIDX=[]
x_5_FIDX.extend(('0','1','2','3','4','5','6','7','8','9'))
x_5_FIDX.extend(('A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z'))
x_5_FIDX.extend(('a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z'))
x_5_FIDX.extend((' ','.',',',':',';','?','!','+','-','\\','/','(',')','@','#','_','=','*','%','<','>'))
x_5_FIDX.extend(('ä','Ä','ö','Ö','ü','Ü'))

# The real character arrays are in the FONT array.
x_5_FONT=[]
x_5_FONT.extend((font_0,font_1,font_2, font_3, font_4, font_5, font_6, font_7, font_8, font_9))
x_5_FONT.extend((font_Ab, font_Bb, font_Cb, font_Db, font_Eb, font_Fb, font_Gb, font_Hb, font_Ib, font_Jb, font_Kb, font_Lb, font_Mb, font_Nb, font_Ob, font_Pb, font_Qb, font_Rb,font_Sb, font_Tb, font_Ub, font_Vb, font_Wb, font_Xb, font_Yb, font_Zb))
x_5_FONT.extend((font_Ab, font_Bb, font_Cb, font_Db, font_Eb, font_Fb, font_Gb, font_Hb, font_Ib, font_Jb, font_Kb, font_Lb, font_Mb, font_Nb, font_Ob, font_Pb, font_Qb, font_Rb,font_Sb, font_Tb, font_Ub, font_Vb, font_Wb, font_Xb, font_Yb, font_Zb))
x_5_FONT.extend((font_SPACE,font_DOT,font_COMMA,font_DBLDOT,font_DBLCOMMA,font_QUESTION,font_EXCLAMATION,font_PLUS,font_MINUS,font_BACKSLASH, font_SLASH,font_BRACEOPEN,font_BRACECLOSE,font_AT,font_HASHTAG,font_UNDERLINE,font_EQUAL,font_TIMES,font_PERCENT,font_LESSER,font_GREATER))
x_5_FONT.extend((font_AEb,font_AEb,font_OEb,font_OEb,font_UEb,font_UEb))
