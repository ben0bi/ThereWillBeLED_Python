# -*- coding: utf-8 -*-

import MySQLdb as SQL

import datetime

now = datetime.datetime.now()                       # hours = 24
thenn = datetime.datetime.now()+datetime.timedelta(days=30)

print "Actual Datetime:"
print str(now)

def openConnection():
	db = SQL.connect(host="localhost",user="BeCal",passwd="ben0biCalendar",db="BeCal",charset="utf8")
	return db

def getCursor(db):
	return db.cursor(SQL.cursors.DictCursor)

def getEventsFromTo(starttime, endtime):
	db = openConnection()
	dbcursor = getCursor(db)
	dbcursor.execute("SELECT * FROM calendarevents WHERE eventtype = '0' AND startdate<='"+str(endtime)+"' AND enddate>='"+str(starttime)+"' ORDER BY startdate ASC")
	count = 0
	for row in dbcursor.fetchall():
		count = count + 1
		rid = row["id"]
		rtitle = row["title"]
		rstartdate = row["startdate"]
		renddate = row["enddate"]
		raudio = row["audiofile"]
		if(raudio!="" and raudio!=0 and raudio!=None):
			raudio="[A] "
		else:
			raudio=" "
		print "[e", rid,"]",raudio, rtitle, " from ", rstartdate, " to ", renddate
	if(count==0):
		print("No entries found.")
	db.close()

def getOpenTodos():
	""" Get all open todos. """
	db = openConnection()
	dbcursor = getCursor(db)
	dbcursor.execute("SELECT * FROM calendarevents WHERE eventtype = '1' ORDER BY startdate ASC")
	count = 0
	for row in dbcursor.fetchall():
		count = count + 1
		rid = row["id"]
		rtitle = row["title"]
		rstartdate = row["startdate"]
		renddate = row["enddate"]
		raudio = row["audiofile"]
		if(raudio!="" and raudio!=0 and raudio!=None):
			raudio="[A] "
		else:
			raudio=" "
		print "[t", rid,"]",raudio, rtitle, " until ", renddate
	if(count==0):
		print("No entries found.")
	db.close()
	return count

def getOpenTodoCount():
	""" Return the count of the open todos. """
	db = openConnection()
	dbcursor = getCursor(db)
	dbcursor.execute("SELECT * FROM calendarevents WHERE eventtype = '1' ORDER BY startdate ASC")
	count = 0
	for row in dbcursor.fetchall():
		count = count + 1
	if(count==0):
		print("No entries found.")
	db.close()
	return count

#####################################################3


print "OPEN TODO COUNT: ", getOpenTodoCount()

print "OPEN Todos: "
getOpenTodos()

print " "
print "Events for the next 30 days:"
getEventsFromTo(now, thenn)

print("Endof Program")
