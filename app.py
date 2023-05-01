from ast import Try
from flask import Flask, render_template, request, redirect, url_for, session
from flask_mysqldb import MySQL
import MySQLdb.cursors
import re
from flask import Flask, request, jsonify
from flask_restful import Resource, Api
import datetime
# from services import sessionService, voucherService, regionService
import os
  
  
app = Flask(__name__)
api = Api(app)

app.secret_key = 'xyzsdfg'
app.config['JSON_SORT_KEYS'] = False

  
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_DB'] = 'skripsi'
  
mysql = MySQL(app)
  
# @app.route('/')
# @app.route('/login', methods =['GET', 'POST'])
# def login():
#     mesage = ''
#     if request.method == 'POST' and 'email' in request.form and 'password' in request.form:
#         result = {}
#         email = request.form['email']
#         password = request.form['password']
#         cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
#         cursor.execute('SELECT * FROM account WHERE email = % s AND password = % s', (email, password, ))
#         user = cursor.fetchone()
#         if user:
#             result['loggedin'] = True
#             result['id'] = user['id']
#             result['username'] = user['username']
#             result['email'] = user['email']
#             mesage = 'Logged in successfully !'
#             # return render_template('user.html', mesage = mesage)

#         else:
#             mesage = 'Please enter correct email / password !'
#     # return render_template('login.html', mesage = mesage)
#         result['mesage'] = mesage
#     return jsonify(result)
  
# @app.route('/logout')
# def logout():
#     session.pop('loggedin', None)
#     session.pop('id', None)
#     session.pop('email', None)
#     return redirect(url_for('login'))
  
# @app.route('/register', methods =['GET', 'POST'])
# def register():
#     mesage = ''
    
#     if request.method == 'POST' and 'username' in request.form and 'password' in request.form and 'email' in request.form :
#         result = {}
#         userName = request.form['username']
#         password = request.form['password']
#         email = request.form['email']
#         cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
#         cursor.execute('SELECT * FROM account WHERE email = % s', (email, ))
#         account = cursor.fetchone()
#         if account:
#             mesage = 'Account already exists !'
#             resp = '99'
#         elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
#             mesage = 'Invalid email address !'
#             resp = '99'
#         elif not userName or not password or not email:
#             mesage = 'Please fill out the form !'
#             resp = '99'
#         else:
#             cursor.execute('INSERT INTO account VALUES (NULL, % s, % s, % s)', (userName, password,email,))
#             # status, result= cursor.executeData('INSERT INTO account VALUES (NULL, % s, % s, % s)', (userName, password,email,))
#             # print(result)
#             # print(status)
#             mysql.connection.commit()
#             mesage = 'You have successfully registered !'
#             resp = '00'
#     elif request.method == 'POST':
#         mesage = 'Please fill out the form !'
#     # return 'username': userName
#     result['response_message'] = mesage
#     result['response_code'] = resp
#     return jsonify(result)
#     # return render_template('register.html', mesage = mesage)

class App(Resource): 
    def post(self,serviceName):
        try:
            # rs = self.rs
            if serviceName =='register':
                result = {}
                userName = request.form['username']
                password = request.form['password']
                email = request.form['email']
                cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
                cursor.execute('SELECT * FROM account WHERE email = % s', (email, ))
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
                    cursor.execute('INSERT INTO account VALUES (NULL, % s, % s, % s)', (userName, password,email,))
                    # status, result= cursor.executeData('INSERT INTO account VALUES (NULL, % s, % s, % s)', (userName, password,email,))
                    # print(result)
                    # print(status)
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
                    rs['response_message'] = 'sukses'
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
    app.run()