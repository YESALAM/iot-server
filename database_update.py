import MySQLdb

db = MySQLdb.connect(host="iot.clbvvfh8xggv.us-east-1.rds.amazonaws.com",
                     user="yesalam",
                     passwd="myIsy269_",
                     )
cur = db.cursor()

cur.execute("""CREATE DATABASE IF NOT EXISTS  iot""")
db.commit()
cur.execute("""USE iot""")
db.commit()
cur.execute("""DROP TABLE IF EXISTS iotdata""")
db.commit()
sql_create  = "CREATE TABLE IF NOT EXISTS iotdata (id int(11) NOT NULL AUTO_INCREMENT, dates varchar(10), times varchar(10), uuid varchar(12),name varchar(25),vrn varchar(10),purpose varchar(50),nop varchar(10),access varchar(10),active boolean,PRIMARY KEY (id));"
cur.execute(sql_create)
db.commit()

