import MySQLdb as SQL

import datetime

now = datetime.datetime.now()
thenn = datetime.datetime.now()+datetime.timedelta(hours=24)

print "Actual Datetime:"
print str(now)

db = SQL.connect(host="localhost",user="BeCal",passwd="ben0biCalendar",db="BeCal")
print("Connection to DB established.")
dbcursor = db.cursor()
dbcursor.execute("SELECT * FROM calendarevents WHERE startdate >= '"+str(now)+"' AND startdate <= '"+str(thenn)+"'")
count = 0
for row in dbcursor.fetchall():
	count = count + 1
	rid = row[0]
	rtitle = row[1]
	rstartdate = row[2]
	renddate = row[3]
	print "[", rid,"] ", rtitle, " from ", rstartdate, " to ", renddate

if(count==0):
	print("No entries found.")
print("Endof Program")

