# BeLED ben0bis LED library
# You can use this lib to create 2 dimensional ws281x LED screens including some LEDs for special functions.
# A typical screen is built like this (here: 5x5 with one Pre-LED and 2 After-LEDs)

# This is, right now, just a mathematical lib. You can use it for other stuff than LEDs, too. ;)

# Here, the first LED is to show the power. The last two LEDs are used to show some status and internet connectivity.
# Between these LEDs is the 5x5 screen. The strip looks like this:
# * pwr ***** ***** ***** ***** ***** * status * inet
# or like this when it is assembled:
# * pwr ***** * status
#       ***** * inet
#       *****
#       *****
#       *****

# Now note that all screen operations, like the masking stuff, ONLY affects the 5x5 screen and NOT the other LEDs.
# Keep that in mind. You will need to take the PRE-Leds into account when using a mask!

# Now for the fonts:
# Import the right font file (here: x*6, where x says that it is of variable width)

# You just need to import the buildtextArray function. All the other stuff will be handled internally.

# from BeFont_x_6.py import buildTextArray_x_6

# The font files consist of arrays with the font characters in pixels, where 0 (o) is not set and 1 (X) is set:
# e.g: A
# oXXoo
# XooXo
# XXXXo
# XooXo
# ooooo

# The files consist of two arrays, one with all the font characters (FONT) and one with all the characters on
# the right index position. The indexes of FONT and FIDX characters must match!

# To get the array of one character, just use getCharArray..(character) from your font file.
# But, as seen above, you just need the buildTextArray.. function.

# Ok, now me make a hello world font text array:

# fontArray = buildTextArray..("Hello World!")

# This array consists of ONE line of text with the character arrays from above, just put together.
# It has x and y array. (The x'es are in the y array): fontArray[y][x], not vice versa!

# Now we make a mask from it.
# A mask is an array in the size of the LED screen (5x5).
# On the mask we set the pixels which are occupied by the font.
# The font is moving on the screen and so it is (also moving) on the mask.

# mymask = createFlatScreenMask(fontArray, myX, myY)

# The FLAT screen mask is just the one dimensional representation of the array instead of a 2-dimensional one.
# The latter (like the text array from above) is used to put the font characters into the right position.
# The first one is (then) used to put this pixels directly on the one-dimensional LED-strip(-array).

# Now you can go through your strip and just check the mask, if it should be coloured. If so, make some fancy color for it.
# Just look at the rainbowCycle function in BeLED.py. Don't forget to take the Pre-LEDs into account!

########################################## THE ACTUAL CODE ##################################################

# BeLED screen configuration
# The screen can have "lights" before and after it on the same line, for lighting other stuff, too, like a power LED.
SCREEN_COUNT_PRE 	= 12	# Number of LEDs before the actual screen. I use one special LED for...special stuff. :)
SCREEN_COUNT_X 		= 10	# Number of LEDs in one line on the screen.
SCREEN_COUNT_Y		= 10	# Number of lines on the screen.
SCREEN_COUNT_AFT	= 0	# Number of LEDs after the actual screen. I just use one at the begin.
SCREEN_DIRECTION 	= 2     # 0 = normal, 1 = y flip, 2 = x flip, 3 = x & y flip
					# This is used for the renderArray function to determine which side of the array faces up.
					# Needed for rendering the fonts in the right direction, my setup is "wrong" for y so I use 1 here.
#SCREEN_ORIENTATION = 0		# 0 = "north", 1 = "south", 2 = "east", 3 = "west"
# (not used right now)		# even if the screen is flipped right, it may be turned into the wrong direction.
							# we turn it with this function.
SCREEN_END_POSITION = (SCREEN_COUNT_PRE + (SCREEN_COUNT_X * SCREEN_COUNT_Y))

# render a screenarray to a mask with the size of the strip screen.
def createScreenMask(screenarray,x,y):
	"""Create a mask (buffer) in screen size and put the screen array on it, moved by x and y"""

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
				# set the pixel.
				if setpix != -1:
					returnarray[ppY][ppX]=setpix
	# return the result.
	return returnarray

# create a one dimensional screen mask.
def createFlatScreenMask(screenarray,x,y):
	"""Create a one dimensional screen mask."""
	mask = createScreenMask(screenarray, x,y)
	ret = []
	for y in range(len(mask)):
		for x in range(len(mask[y])):
			ret.append(mask[y][x])
	return ret

# create a combined flat mask with ORed values (1,1=1 / 0,1=1 / 1,0=1, 0,0=0)
# the two mask arrays must have the same size. But this will not be a problem as long as you don't
# change the screen size in mid-program. Masks are created based on the real screen size,
# not on the given input size.
def combineFlatScreenMasks_OR(mask1, mask2):
	result = []
	for i in range(len(mask1)):
		if mask1[i]==1 or mask2[i]==1:
			result.append(1)
		else:
			result.append(0)
	return result
