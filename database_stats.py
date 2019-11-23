import sqlite3
from datetime import datetime
from urllib.request import pathname2url

dbFileName = "Logs.db"
connectionTableName = "ConnectionLogs"


# Initialize Database
# Credit to https://stackoverflow.com/questions/12932607/how-to-check-if-a-sqlite3-database-exists-in-python
conn = None
try:
    dburi = 'file:{}?mode=rw'.format(pathname2url(dbFileName))
    conn = sqlite3.connect(dburi, uri=True)
except sqlite3.OperationalError:
    # handle missing database case
    quit()

curs = conn.cursor()
# curs.execute("DROP TABLE " + connectionTableName) # TODO debug only
curs.execute("CREATE TABLE IF NOT EXISTS " + connectionTableName + " (cookie STRING PRIMARY KEY, firstAccessDate BIGINT, numValidMoves INT);")
conn.commit()

cookie = 'xxxxxxxx-xxxx-Mxxx-Nxxx-xxxxxxxxxxxx'

# curs.execute("INSERT INTO " + connectionTableName + " (cookie, firstAccessDate, numValidMoves) VALUES (?,?,?)", (cookie, datetime.today().timestamp(), 3))
# curs.execute("UPDATE " + connectionTableName + " SET numValidMoves=numValidMoves+1 WHERE cookie=?", (cookie,))
# curs.execute("SELECT COUNT(*) FROM " + connectionTableName + " WHERE cookie=?;", (cookie,))

curs.execute("SELECT COUNT(*) FROM " + connectionTableName)
count = curs.fetchone()

print("Stats for Table \"%s\"\n\n" % connectionTableName)
print("Executing SQL Query \" %s \"..." % ("SELECT * FROM " + connectionTableName))
print("Number of rows is: " + str(count[0]))
for row in curs.execute("SELECT * FROM " + connectionTableName):
    print("Cookie: %s;\t Date First Accessed: %s \t Number Valid Clicks: %s" % \
        (row[0], datetime.fromtimestamp(row[1]).strftime("%Y-%m-%d %H:%M:%S"), row[2]))

conn.commit()