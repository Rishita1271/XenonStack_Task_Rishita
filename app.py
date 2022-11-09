from flask import Flask, render_template, request, redirect, url_for, session
from flask_mysqldb import MySQL
import MySQLdb.cursors
import re
  
app = Flask(__name__)
  
app.secret_key = 'xyzsdfg'
  
app.config['MYSQL_HOST'] = '127.0.0.1'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'user_system'
  
mysql = MySQL(app)


@app.route('/')
def hello():
    return render_template('home.html')

@app.route('/Sign In', methods =['GET', 'POST'])
def login():
    mesage = ''
    if request.method == 'POST' and 'email' in request.form and 'password' in request.form:
        email = request.form['email']
        password = request.form['password']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM user WHERE email = % s AND password = % s', (email, password, ))
        user = cursor.fetchone()
        if user:
            session['loggedin'] = True
            session['userid'] = user['userid']
            session['name'] = user['name']
            session['email'] = user['email']
            mesage = 'Logged in successfully !'
            return render_template('home2.html', mesage = mesage)
        else:
            mesage = 'Please enter correct email / password !'
    return render_template('login.html', mesage = mesage)
  
@app.route('/logout')
def logout():
    session.pop('loggedin', None)
    session.pop('userid', None)
    session.pop('email', None)
    return redirect(url_for('hello'))
  
@app.route('/Sign Up', methods =['GET', 'POST'])
def register():
    mesage = ''
    if request.method == 'POST' and 'name' in request.form and 'password' in request.form and 'email' in request.form :
        userName = request.form['name']
        password = request.form['password']
        email = request.form['email']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM user WHERE email = % s', (email, ))
        account = cursor.fetchone()
        if account:
            mesage = 'Account already exists !'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            mesage = 'Invalid email address !'
        elif not userName or not password or not email:
            mesage = 'Please fill out the details !'
        else:
            cursor.execute('INSERT INTO user VALUES (NULL, % s, % s, % s)', (userName, email, password, ))
            mysql.connection.commit()
            mesage = 'You have successfully registered ! Login Now!'
    elif request.method == 'POST':
        mesage = 'Please fill out the details !'
    return render_template('register.html', mesage = mesage)

@app.route('/Contact Us', methods =['GET', 'POST'])
def contact():
    mesage = ''
    if request.method == 'POST' and 'name' in request.form and 'query' in request.form and 'contact' in request.form:
        userName = request.form['name']
        query = request.form['query']
        contact = request.form['contact']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        if not re.match(r'^[0-9]', contact) or len(contact) != 10:
            mesage = 'Invalid Contact Number !'
        elif not userName or not query or not contact:
            mesage = 'Please fill out the details !'
        else:
            cursor.execute('INSERT INTO contact VALUES (NULL, % s, % s, % s)', (userName, contact, query, ))
            mysql.connection.commit()
            mesage = 'We will contact you! Go to Home Page now!'
    elif request.method == 'POST':
        mesage = 'Please fill out the details !'
    return render_template('contactus.html', mesage = mesage)
    
if __name__ == "__main__":
    app.run()