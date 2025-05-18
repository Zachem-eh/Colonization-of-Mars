import sqlite3

com = sqlite3.connect('database/mars_explorer.db')
cur = com.cursor()

sql = '''INSERT INTO hazards(id,title) VALUES(1,'Danger')'''
cur.execute(sql)
sql = '''INSERT INTO hazards(id,title) VALUES(2,'Normal')'''
cur.execute(sql)
sql = '''INSERT INTO hazards(id,title) VALUES(3,'Easy')'''
cur.execute(sql)
com.commit()