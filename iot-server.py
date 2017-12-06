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
cur.execute("use iot;")


@app.route('/')
def hello_world():
    return 'Hello World!'


@app.route('/fetch',methods=['GET','POST'])
def fetch():
    print "Fetch called"
    uuid = request.form['uuid']
    bid = request.form['b_id']
    date = datetime.datetime.now().strftime("%y-%m-%d")
    print "fetch called with",bid,uuid
    sql_check = "Select * from iotdata where dates ='" + date + "' and uuid = '" + uuid + "' and active=0"
    cur.execute(sql_check)

    try:
        a = cur.fetchone()
        if a == None:
            print "card not registerd"
            return '{"result":"not registered"}'
        else:
            access = a[8]
            #check for this access
            if access == '1' and bid=='1':
                return '{"result":"ok"}'
            elif access == '2' and (bid=='1' or bid=='2'):
                return '{"result":"ok"}'
            elif access == '3' and bid =='3':
                return '{"result":"ok"}'
            elif access == '10' and bid=='10':
                return '{"result":"ok"}'
            elif access == '5' and bid=='5':
                return '{"result":"ok"}'
            elif access == '8' and bid=='8':
                return '{"result":"ok"}'
            elif access == '9' and bid=='9':
                return '{"result":"ok"}'
            elif access =='7' and (bid=='9' or bid=='7'):
                return '{"result":"ok"}'
            elif access =='4' and bid=='4':
                return '{"result":"ok"}'
            elif access == '6' and (bid=='6' or bid == '11'):
                return '{"result":"ok"}'
            else:
                return '{"result":"notok"}'




    except:
        print "Some error"
        return '{"result":"error"}'
    

@app.route('/register',methods=['GET','POST'])
def register():
    print "Register called"
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
                    return '{"result":"ok"}'
                except ValueError:
                    print "insert error"
                    return '{"result":"error"}'
                    db.rollback()
            else:
                print "Already Generated"
                return '{"result":"already"}'
        except:
            print "Some error"
            return '{"result":"error"}'

@app.route('/gateexit',methods=['GET','POST'])
def gateExit():
    print "Gate Exit called"
    if request.method == 'POST':
        uuid = request.form['uuid']
        date = datetime.datetime.now().strftime("%y-%m-%d") 

	sql_check = "Select * from iotdata where dates ='"+date+"' and uuid = '"+uuid+"' and active=1"
        cur.execute(sql_check)

        try:
            a = cur.fetchone()
            if a == None:
                sql_update = "update iotdata set active=1 where dates ='"+date+"' and uuid = '"+uuid+"'"
                try:
                    cur.execute(sql_update)
                    db.commit()
                    return '{"result":"ok"}'
                except ValueError:
                    print "Update error"
                    return '{"result":"updateerror"}'
                    db.rollback()
            else:
                print "Already Updated"
                return '{"result":"already"}'
        except:
            print "Some error"
            return '{"result":"error"}'
       

if __name__ == '__main__':
    app.run(host='0.0.0.0')
