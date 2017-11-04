from flask import Flask
from flask import request

import MySQLdb

import datetime
import time

app = Flask(__name__)

db = MySQLdb.connect(host="iot.clbvvfh8xggv.us-east-1.rds.amazonaws.com",
                     user="yesalam",
                     passwd="myIsy269_",
                     )

cur = db.cursor()

def createTable():
    cur.execute("""CREATE DATABASE IF NOT EXISTS  iot""")
    db.commit()
    sql_create  = "CREATE TABLE IF NOT EXISTS iotdata (id int(11) NOT NULL AUTO_INCREMENT, dates varchar(10), times varchar(10), uuid varchar(10),name varchar(25),vrn varchar(10),purpose varchar(50),nop varchar(10),access varchar(10),active boolean,PRIMARY KEY (id));"
    cur.execute(sql_create)
    db.commit()

def dropTable():
    cur.execute("""DROP TABLE IF EXISTS iotdata""")
    db.commit()

@app.route('/')
def hello_world():
    return 'Hello World!'

@app.route('/create')
def create():
    createTable()
    return 'Success'

@app.route('/fetch',methods=['GET','POST'])
def fetch():
    uuid = request.form['uuid']
    date = datetime.datetime.now().strftime("%y-%m-%d")

    sql_check = "Select * from iotdata where dates ='" + date + "' and uuid = '" + uuid + "' and active=0"
    cur.execute(sql_check)

    try:
        a = cur.fetchone()
        if a == None:
            return "{'result':'not registered'}"
        else:
            access = a[8]
            #check for this access



    except:
        print "Some error"
        return "{'result':'error'}"

    return 'hello'

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

        sql_check = "Select * from iotdata where dates ='"+date+"' and uuid = '"+uuid+"' and active=0"
        cur.execute(sql_check)

        try:
            a = cur.fetchone()
            if a == None:
                sql_insert = "insert into iotdata(dates,times,uuid,name,vrn,purpose,nop,access,active) VALUES('" + date + "','" + time + "','" + uuid + "','" + name + "','" + vrn + "','" + purpose + "','" + nop + "','" + access + "','0')"
                try:
                    cur.execute(sql_insert)
                    db.commit()
                    return "{'result':'ok'}"
                except ValueError:
                    print "insert error"
                    return "{'result':'error'}"
                    db.rollback()
            else:
                print "Already Authenticated"
                return "{'result':'already'}"
        except:
            print "Some error"
            return "{'result':'error'}"






if __name__ == '__main__':
    app.run(host='0.0.0.0')
