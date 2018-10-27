# GPIO Menu Stuff for the LED display.
# There are two buttons: one for the main menu and one for the corresponding sub menu.

import RPi.GPIO as GPIO

# MAINMENU ITEMS:
# Name, Symbol, Function (State)
MAINMENU_ARRAY = [
["OFF","0","off"],
["Clock","1","clock"],
["Calendar", "2","calendar"],
["Solar System","3","solsystem"],
["Light","4","light"]
]

# The GPIO BCM numbers of the buttons to switch trough the menu items.
BCM_BTN_MAINMENU = 17		# Button number for the main menu
BCM_BTN_SUBMENU = 27		# Button number for the submenu
BCM_BTNPRESS_MAINMENU = 0	# Is the button already down?
BCM_BTNPRESS_SUBMENU = 0	# -"- ?

# Menu item stuff.
ACTUAL_MENU_ITEM = 0 	# Which menu is acutally on? Set to -1 for first first, else it is second first (at start of program)
OLD_MENU_ITEM = 0		# Does the symbol and other stuff have to change?
ACTUAL_SUBMENU_ITEM = 0 # Same for the submenu.

# Menu Variables for display.
MENU_SHOW_TIME = 2.0	# How many seconds to show the menu entry?
MENU_CHANGED_TIME = 0.0	# Set the seconds to show the menu here.
# It will count down to 0 and then show the function.

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
	global OLD_MENU_ITEM, ACTUAL_MENU_ITEM
	# reset the old menu item.
	OLD_MENU_ITEM = ACTUAL_MENU_ITEM
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
		MENU_CHANGED_TIME = MENU_SHOW_TIME		
	else:
		ACTUAL_SUBMENU_ITEM = ACTUAL_SUBMENU_ITEM + 1
		MENU_CHANGED_TIME = 0 # Just continue when pressed.
	
	print("Menu selection: "+str(ACTUAL_MENU_ITEM)+" Submenu: "+str(ACTUAL_SUBMENU_ITEM))

# return the changetime. If >0, render the menu.
def getMenuChangeTime():
	global MENU_CHANGED_TIME
	return MENU_CHANGED_TIME

# update the changetime.	
def updateMenuChangeTime(frametime):
	global MENU_CHANGED_TIME
	if MENU_CHANGED_TIME>0.0:
		MENU_CHANGED_TIME = MENU_CHANGED_TIME - frametime
	else:
		MENU_CHANGED_TIME = 0.0;

# return the actual main menu item index.
def getActualMenuItem():
	global ACTUAL_MENU_ITEM
	return ACTUAL_MENU_ITEM

# return the actual menu item function
def getActualMenuItemFunction():
	global ACTUAL_MENU_ITEM, MAINMENU_ARRAY
	if ACTUAL_MENU_ITEM<0:
		return -1
	# return the button state.
	return MAINMENU_ARRAY[ACTUAL_MENU_ITEM][2]	

# return the actual sub menu item
def getActualSubmenuItem():
	global ACTUAL_SUBMENU_ITEM
	return ACTUAL_SUBMENU_ITEM
	
# set the submenu item.
def setActualSubmenuItem(itm):
	global ACTUAL_SUBMENU_ITEM
	ACTUAL_SUBMENU_ITEM = itm
	return ACTUAL_SUBMENU_ITEM
	
# return the count of items in the main menu.
def getMainMenuCount():
	global MAINMENU_ARRAY
	return len(MAINMENU_ARRAY)

# has the menu changed?
def menuHasChanged():
	global OLD_MENU_ITEM, ACTUAL_MENU_ITEM
	if OLD_MENU_ITEM!=ACTUAL_MENU_ITEM:
		return 1
	return 0

# clean the GPIO status.
def cleanupGPIO():
	GPIO.cleanup()