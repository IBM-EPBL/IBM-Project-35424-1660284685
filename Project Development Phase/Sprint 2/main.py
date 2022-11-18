from flask import Flask, render_template, request, session
import ibm_db
import re

app = Flask(__name__)

app.secret_key = 'a'

conn = ibm_db.connect("DATABASE=bludb;HOSTNAME=125f9f61-9715-46f9-9399-c8177b21803b.c1ogj3sd0tgtu0lqde00.databases.appdomain.cloud;PORT=30426;SECURITY=SSL;SSLServerCertificate=Certificate.crt;UID=cft48447;PWD=xQ7cUsF9avQJdt72",'','')

@app.route('/')
def home():
    return render_template('login.html')

@app.route('/login', methods = ["GET", "POST"])
def login():
    global userid
    msg=''
    if request.method == 'POST':
        username = request.form["username"]
        password = request.form["pass"]
        sql = "SELECT * FROM USER_DETAILS WHERE username =? AND password =?"
        stmt = ibm_db.prepare(conn, sql)
        ibm_db.bind_param(stmt,1,username)
        ibm_db.bind_param(stmt,2,password)
        ibm_db.execute(stmt)
        account = ibm_db.fetch_assoc(stmt)
        print(account)
        if account :
            session['loggedin'] = True
            session['id'] = account['USERNAME']
            userid = account['USERNAME']
            session['username'] = account['USERNAME']
            msg = 'Logged in Successfully !'
            return render_template('dashboard.html',msg = msg)
        else :
            msg = 'Incorrect username / password !'
    return render_template('login.html', msg = msg)

@app.route('/signup', methods = ['GET','POST'])
def signup():
    msg = ''
    if request.method == "POST" :
        name = request.form["Name"]
        username = request.form['username']
        password = request.form["pass"]
        bloodgroup = request.form['blood_group']
        email = request.form["email"]
        phone_number = request.form['phnumber']
        gender = request.form['gender']
        age = request.form['age']
        sql = "SELECT * FROM USER_DETAILS WHERE username =?"
        stmt = ibm_db.prepare(conn,sql)
        ibm_db.bind_param(stmt,1,username)
        ibm_db.execute(stmt)
        account = ibm_db.fetch_assoc(stmt)
        print(account)
        if account:
            msg = "Account Already Exists !"
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            msg = "Invalid Email Address !"
        elif not re.match(r'[A-Za-z0-9]+', username):
            msg = "Username must contain character and numbers !"
        else:
            insert_sql = "INSERT INTO USER_DETAILS VALUES (?,?,?,?,?,?,?,?)"
            prep_stmt = ibm_db.prepare(conn, insert_sql)
            ibm_db.bind_param(prep_stmt,1,name)
            ibm_db.bind_param(prep_stmt,2,username)
            ibm_db.bind_param(prep_stmt,3,password)
            ibm_db.bind_param(prep_stmt,4,bloodgroup)
            ibm_db.bind_param(prep_stmt,5,email)
            ibm_db.bind_param(prep_stmt,6,phone_number)
            ibm_db.bind_param(prep_stmt,7,gender)
            ibm_db.bind_param(prep_stmt,8,age)
            ibm_db.execute(prep_stmt)
            msg = "You Have Successfully Registred !."
    elif request.method == "POST":
        msg = "Please Fill out the form !"
    return render_template('signup.html',msg = msg)

@app.route('/dashboard')
def dash():
    return render_template('dashboard.html')

@app.route('/display')
def display():
    print(session['username'],session['id'])
    cursor = mysql.connection.cursor()
    cursor.execute('SELECT * FROM user_detail WHERE username = %s', (session['id']))
    account = cursor.fetchone()
    print("AccountDisplay", account)
    return render_template('display.html', account = account)

@app.route('/logout')
def logout():
    session.pop('loggedIn',None)
    session.pop('username',None)
    return render_template('login.html')

if __name__ == "__main__":
    app.run(host='0.0.0.0',debug='TRUE')