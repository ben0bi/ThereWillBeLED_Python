import MySQLdb as SQL

db = SQL.connect(host="localhost",user="BeCal",passwd="ben0biCalendar",db="BeCal")
print("Connection to DB established.")
dbcursor = db.cursor()
dbcursor.execute("SELECT * FROM calendarevents")
for row in dbcursor.fetchall():
	print row[0]," ", row[1]

print("Endof Program")

