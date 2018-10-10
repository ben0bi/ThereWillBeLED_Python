# ThereWillBeLED_Python
Font render engine using the ws281x library from jgarff https://github.com/jgarff/rpi_ws281x

# BeLED ben0bis LED library
You can use this lib to create 2 dimensional ws281x LED screens including some LEDs for special functions.
A typical screen is built like this (here: 5x5 with one Pre-LED and 2 After-LEDs)

This is, right now, just a mathematical lib. You can use it for other stuff than LEDs, too. ;)

Here, the first LED is to show the power. The last two LEDs are used to show some status and internet connectivity.
Between these LEDs is the 5x5 screen. The strip looks like this:
* pwr ***** ***** ***** ***** ***** * status * inet

or like this when it is assembled:
* pwr ***** * status  
      ***** * inet  
      *****  
      *****  
      *****  

Now note that all screen operations, like the masking stuff, ONLY affects the 5x5 screen and NOT the other LEDs.
Keep that in mind. You will need to take the PRE-Leds into account when using a mask!

Now for the fonts:
Import the right font file (here: x*6, where x says that it is of variable width)

You just need to import the buildtextArray function. All the other stuff will be handled internally.

from BeFont_x_6.py import buildTextArray_x_6

The font files consist of arrays with the font characters in pixels, where 0 (o) is not set and 1 (X) is set:
e.g: A  
oXXoo  
XooXo  
XXXXo  
XooXo  
ooooo  

The files consist of two arrays, one with all the font characters (FONT) and one with all the characters on
the right index position. The indexes of FONT and FIDX characters must match!

To get the array of one character, just use getCharArray..(character) from your font file.
But, as seen above, you just need the buildTextArray.. function.

Ok, now me make a hello world font text array:

fontArray = buildTextArray..("Hello World!")

This array consists of ONE line of text with the character arrays from above, just put together.
It has x and y array. (The x'es are in the y array): fontArray[y][x], not vice versa!

Now we make a mask from it.
A mask is an array in the size of the LED screen (5x5). 
On the mask we set the pixels which are occupied by the font.
The font is moving on the screen and so it is (also moving) on the mask.

mymask = createFlatScreenMask(fontArray, myX, myY)

The FLAT screen mask is just the one dimensional representation of the array instead of a 2-dimensional one.
The latter (like the text array from above) is used to put the font characters into the right position.
The first one is (then) used to put this pixels directly on the one-dimensional LED-strip(-array).

Now you can go through your strip and just check the mask, if it should be coloured. If so, make some fancy color for it.
Just look at the rainbowCycle function in BeLED.py. Don't forget to take the Pre-LEDs into account!