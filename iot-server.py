from flask import Flask
from flask import request

import MySQLdb

import datetime
import time

app = Flask(__name__)

db = MySQLdb.connect(host="localhost",
                     user="root",
                     passwd="myIsy269",
                     )

cur = db.cursor()

def createTable():
    cur.execute("""CREATE DATABASE IF NOT EXISTS  iot""")
    db.commit()
    sql_create  = "CREATE TABLE IF NOT EXISTS iotdata (id int(11) NOT NULL AUTO_INCREMENT, dates varchar(10), times varchar(10), uuid varchar(10),name varchar(10),vrn varchar(10),purpose varchar(10),nop varchar(10),access varchar(10),active boolean,PRIMARY KEY (id));"
    cur.execute(sql_create)
    db.commit()


@app.route('/')
def hello_world():
    return 'Hello World!'

@app.route('/register',methods=['GET','POST'])
def register():

    if request.method == 'POST':
        name = request.form['name']
        vrn = request.form['vrn']
        nop = request.form['nop']
        purpose = request.form['purpose']
        access = request.form['access']
        uuid = request.form['token_id_button']

        date = datetime.datetime.now().strftime("%y-%m-%d")
        time = datetime.datetime.now().strftime("%H-%M")

        sql_check = "Select * from iotdata where dates ='"+date+"' and uuid = '"+uuid+"' and active=1"
        cur.execute(sql_check)

        (number_of_rows,) = cur.fetchone()
        if number_of_rows>0:
            #some error
            print "Already registered"
        else:
            sql_insert = "insert into iotdata(dates,times,uuid,name,vrn,purpose,nop,access,active) VALUES('"+date+"','"+time+"','"+uuid+"','"+name+"','"+vrn+"','"+purpose+"','"+nop+"','"+purpose+"','0')"
            try:
                cur.execute(sql_insert)
                db.commit()
            except:
                db.rollback()






if __name__ == '__main__':
    app.run()
