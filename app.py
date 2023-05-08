from ast import Try
from flask import Flask, render_template, request, redirect, url_for, session
from flask_mysqldb import MySQL
import MySQLdb.cursors
import re
from flask import Flask, request, jsonify
from flask_restful import Resource, Api
import datetime
# from flask_bcrypt import Bcrypt
# from services import sessionService, voucherService, regionService
import os 

  
app = Flask(__name__)
api = Api(app)
# bcrypt = Bcrypt(app)s

app.secret_key = 'filtra@fdl'
app.config['JSON_SORT_KEYS'] = False

  
app.config['MYSQL_HOST'] = '194.163.42.201'
app.config['MYSQL_USER'] = 'filt9288_pramono'
app.config['MYSQL_PASSWORD'] = 'Luthfisangaji2301'
app.config['MYSQL_DB'] = 'filt9288_filtration_detergent_laundry'
# app.config['MYSQL_HOST'] = 'localhost'
# app.config['MYSQL_USER'] = 'root'
# app.config['MYSQL_PASSWORD'] = ''
# app.config['MYSQL_DB'] = 'filtration_detergent_laundry'
mysql = MySQL(app)

class App(Resource): 
    def post(self,serviceName):
        try:
            # rs = self.rs
            rs = {'response_code': '', 'response_message': '','date_process': '', 'data': []}
            if serviceName == 'login':
                result = {}
                username = request.form['ua_username']
                password = request.form['ua_password']
                cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
                cursor.execute('SELECT * FROM user_account WHERE ua_username = % s AND ua_password = % s', (username, password, ))
                user = cursor.fetchone()
                if user:
                    result['ua_create_date'] = user['ua_create_date']
                    result['loggedin'] = True
                    result['id'] = user['ua_id']
                    result['username'] = user['ua_username']
                    result['email'] = user['ua_email']
                    rs['data'].append(result)
                    rs['response_code'] = '00'
                    rs['response_message'] = 'Successs'
                    rs['date_process'] = datetime.datetime.now()
                    # return render_template('user.html', mesage = mesage)

                else:
                    rs['response_code'] = '99'
                    rs['response_message'] = "username/password doesn't match"
                return jsonify(rs)
            
            elif serviceName =='register':
                result = {}
                userName = request.form['ua_username']
                email = request.form['ua_email']
                password = request.form['ua_password']
                # password = 'hunter2'
                # pw_hash = bcrypt.generate_password_hash(password)
                cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
                print(cursor)
                cursor.execute('SELECT * FROM user_account WHERE ua_email = % s', (email, ))
                account = cursor.fetchone()
                if account:
                    mesage = 'Account already exists !'
                    resp = '99'
                elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
                    mesage = 'Invalid email address !'
                    resp = '99'
                elif not userName or not password or not email:
                    mesage = 'Please fill out the form !'
                    resp = '99'
                else:
                    cursor.execute('INSERT INTO user_account VALUES (NULL, % s, % s, % s,NOW())', (userName,email,password))
                    mysql.connection.commit()
                    mesage = 'You have successfully registered !'
                    resp = '00'
                    # return jsonify(self)
                result['response_message'] = mesage
                result['response_code'] = resp
                return jsonify(result)
        except Exception as e:
            # common.write_log_error(str(e))
            return jsonify({'Error': str(e)})

    def get(self,serviceName):
        try:
            rs = {'response_code': '', 'response_message': '','date_process': '', 'data': []}

            if serviceName == 'arduino':
                
                cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
                cursor.execute('SELECT * FROM arduino_value')
                av = cursor.fetchall() 
                if av != '' :
                    rs['response_code'] = '00'
                    rs['response_message'] = 'Successs'
                    rs['date_process'] = datetime.datetime.now()
                    for row in av:
                        result = {} 
                        result['av_id'] = row['av_id']
                        result['temperatur'] = row['av_temperatur']
                        result['acidity'] = row['av_acidity']
                        result['turbidity'] = row['av_turbidity']
                        result['tds'] = row['av_tds']
                        result['av_create_date'] = row['av_create_date']
                        # print(row['av_id'])
                        rs['data'].append(result)   
                    return jsonify(rs)
                else : 
                    return jsonify({"response_message": "data tidak ada", "response_code": "99", "data": []})

                
                
        except Exception as e:
            return jsonify({'Error': str(e)})

api.add_resource(App, '/<string:serviceName>')
if __name__ == "__main__":
    # app.run()
    # app.run(host='194.163.42.210', port=3060, debug=True)
    app.run(host='0.0.0.0', port=3060, debug=True)