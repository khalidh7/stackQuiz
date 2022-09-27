import os

from flask import Flask, render_template, url_for, request, g, redirect, session
from database import connect_to_database, getDatabase
from werkzeug.security import generate_password_hash, check_password_hash
import os


app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(24)

def getCurrentUser():
    user_result = None
    if 'user' in session:
        user = session['user']
        db = getDatabase()
        user_cursor = db.execute("select * from users where name = ?", [user])
        user_result = user_cursor.fetchone()
    return user_result

@app.teardown_appcontext
def close_db(error):
    if hasattr(g, 'quizapp_db'):
        g.quizapp_db.close()

@app.route('/')
def index():
    user = getCurrentUser()
    loggedin = False
    loginneeded = False
    if session:
        loggedin = True
    else:
        loginneeded = True

    return render_template("home.html", user = user, loginneeded = loginneeded, loggedin = loggedin)


@app.route('/login', methods=["POST" , "GET"])
def login():
    user = getCurrentUser()
    error = None

    if request.method == "POST":
        name = request.form['name']
        password = request.form['password']

        db = getDatabase()
        tempUser = db.execute("select * from users where name = ?", [name])
        tempdbUser =  tempUser.fetchone()

        if tempdbUser:
            if check_password_hash(tempdbUser['password'], password):
                session['user'] = tempdbUser['name']
                return redirect(url_for('index'))
            else:
                error = "Username or password incorrect. Please try again."
                return render_template('login.html', error = error)
        else:
            error = "Username or password incorrect. Please try again."
            return render_template('login.html', error = error)

    return render_template("login.html", user = user, error = error)

@app.route('/register', methods=["POST", "GET"])
def register():
    user = getCurrentUser()
    error = None
    if request.method == "POST":
        db = getDatabase()
        name = request.form['name']
        password = request.form['password']

        uCursor = db.execute("select * from users where name = ?", [name])
        existingU = uCursor.fetchone()
        if existingU:
            error = "Username already taken, please use a different username."
            return render_template("register.html", error = error)

        hashed_password = generate_password_hash(password, method='sha256')
        db.execute("insert into users (name, password) values (?,?)", [name, hashed_password])
        db.commit()
        session['user'] = name
        return redirect(url_for('index'))


    return render_template("register.html", user = user)

@app.route('/quiz', methods = ["POST", "GET"])
def quiz():
    user = getCurrentUser()
    lang = None
    if request.method == "POST":
        typeStack = request.form['typeStack']
        dbc = request.form['dbq']
        lang = request.form['language']
        platform = request.form['op']
        return render_template("results.html", typeStack = typeStack, dbc = dbc, lang = lang, platform = platform)


    return render_template("quiz.html", user = user)













@app.route('/results')
def results(typeStack, dbc, lang, platform):
    user = getCurrentUser()
    dba = None
    extras = None
    if typeStack == 'frontend':
        if platform == 'ios':
            lang = 'Swift is the industry standard when it comes to iOS development.'
            ide = 'XCode is the best editor to develop and iOS application.'
            extras = 'Swift and XCode can be used for front-end, back-end, or both.'
            return render_template('results.html', language=lang, ide=ide, dba=dba, extras=extras)
        elif platform == 'android':
            lang = 'Java and Kotlin are the best languages to create an Android APK.'
            ide = "Android Studio by JetBrains is a great choice due to its support for Android Development and its Android Emulator"
            return render_template('results.html', language = lang, ide = ide, dba = dba, extras = extras)


















@app.route('/logout')
def logout():
    if session:
        session.popitem()
    return redirect(url_for('index'))

if __name__ == "__main__":
    app.run(debug=True)