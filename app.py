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
    langa= None
    idea = None
    dba = None
    extras = None
    typeStack = None
    dbc = None
    lang = None
    platform = None
    if request.method == "POST":
        typeStack = request.form['typeStack']
        dbc = request.form['dbq']
        lang = request.form['language']
        platform = request.form['op']
        if typeStack and dbc and lang and platform:
            if typeStack == 'frontend':
                if platform == 'ios':
                    langa = 'Swift is the industry standard when it comes to iOS development.'
                    idea = 'XCode is the best editor to develop and iOS application.'
                    extras = 'Swift and XCode can be used for front-end, back-end, or both.'
                    dba = None
                if platform == 'android':
                    langa = 'Java and Kotlin are the best languages to create an Android APK.'
                    idea = "Android Studio by JetBrains is a great choice due to its support for Android Development and its Android Emulator"
                    dba = None
                    extras = None
                if platform == 'website':
                    if lang == 'python' or lang == 'java':
                        langa = 'Using frameworks like Flask and Django, you can create a website using Python.'
                        idea = 'VS Code is one of the best code editors you can use for a Python web application. However PyCharm by JetBrains is a still a great choice.'
                        dba = None
                        extras = 'If you are still new to web development, it is recommended to use Flask. Once you gain more experience try creating something usuing Django.'

                    if lang == 'javascript':
                        langa = 'The best place to start with web development is the HTML/CSS/Javascript framework. Once you get more comfortble try using a Javascript framework like React.js or Angular.'
                        idea = 'VS Code and PhpStorm are both great options'
                        dba= None
                        extras = None
                if platform == 'os':
                    if lang == 'python':
                        langa = 'Python is a very powerful programming language due to its extensive libraries and simple syntax.'
                        idea = 'VS Code and PyCharm are both great options.'
                        dba = None
                        extras = None
                    if lang == 'java' or lang == 'javascript':
                        langa = 'Java is a great language first language to learn. Its syntax is not supe hard to learn but it is difficult enough to challenge you.'
                        idea = 'IntelliJ IDEA by JetBrains is a great IDE to use with Java due to its support for Java development'
                        dba = None
                        extras = None
            if typeStack == 'backend':
                if platform == 'android':
                    if dbc == 'hosteddb':
                        langa = 'Java / PHP'
                        idea = 'Android Studio'
                        dba = 'MySQL'
                        extras = 'Create a REST API using a Linux, Apache, MySQL, PHP stack. Use the retrofit library to create HTTP requests. Gradle project recommended.'
                    if dbc == 'localdb':
                        langa = 'Java'
                        idea = 'Android Studio'
                        dba = 'Sqlite'
                        extras = 'Sqlite is a local database stored on your devices hard drive. No internet access is required to use Sqlite database.'
                    if dbc == 'nodb':
                        langa = 'Java'
                        idea = 'Android Studio'
                        dba = None
                        extras = None
                if platform == 'ios':
                    if dbc == 'hosteddb':
                        langa = 'Swift'
                        idea = 'XCode'
                        dba = 'MySQL'
                        extras = None
                    if dbc == 'localdb':
                        langa = 'Swift'
                        idea = 'XCode'
                        dba = 'Sqlite'
                        extras = 'Sqlite is a local database stored on your devices hard drive. No internet access is required to use Sqlite database.'
                    if dbc == 'nodb':
                        langa = 'Swift'
                        idea = 'XCode'
                        dba = None
                        extras = None
                if platform == 'os' or platform == 'website':
                    if dbc == 'hosteddb':
                        if lang == 'python':
                            langa = 'Python is a very powerful programming language due to its extensive libraries and simple syntax.'
                            idea = 'VS Code and PyCharm are both great options.'
                            dba = 'MySQL'
                            extras = None
                        if lang == 'java' or lang == 'javascript':
                            langa = 'Java is a great language first language to learn. Its syntax is not supe hard to learn but it is difficult enough to challenge you.'
                            idea = 'IntelliJ IDEA by JetBrains is a great IDE to use with Java due to its support for Java development'
                            dba = 'MySQL'
                            extras = None
                    if dbc == 'localdb':
                        if lang == 'python':
                            langa = 'Python is a very powerful programming language due to its extensive libraries and simple syntax.'
                            idea = 'VS Code and PyCharm are both great options.'
                            dba = 'Sqlite'
                            extras = None
                        if lang == 'java' or lang == 'javascript':
                            langa = 'Java is a great language first language to learn. Its syntax is not supe hard to learn but it is difficult enough to challenge you.'
                            idea = 'IntelliJ IDEA by JetBrains is a great IDE to use with Java due to its support for Java development'
                            dba = 'Sqlite'
                            extras = None
                    if dbc == 'nodb':
                        if lang == 'python':
                            langa = 'Python is a very powerful programming language due to its extensive libraries and simple syntax.'
                            idea = 'VS Code and PyCharm are both great options.'
                            dba = None
                            extras = None
                        if lang == 'java' or lang == 'javascript':
                            langa = 'Java is a great language first language to learn. Its syntax is not supe hard to learn but it is difficult enough to challenge you.'
                            idea = 'IntelliJ IDEA by JetBrains is a great IDE to use with Java due to its support for Java development'
                            dba = None
                            extras = None
            if typeStack == 'both':
                if platform == 'ios':
                    langa = 'Swift'
                    idea = 'XCode'
                    if dbc == 'hosteddb':
                        dba = 'MySQL'
                    if dbc == 'localdb':
                        dba = 'Sqlite'
                    if dbc == 'nodb':
                        dba = None
                    extras = None
                if platform == 'android':
                    langa = 'Java'
                    idea = 'Android Studio'
                    if dbc == 'hosteddb':
                        dba = 'MySQL'
                    if dbc == 'localdb':
                        dba = 'Sqlite'
                    if dbc == 'nodb':
                        dba = None
                    extras == None
                if platform == 'website':
                    langa = 'Javascript (Node.js, React.js)'
                    idea = 'Visual Studio'
                    if dbc == 'hosteddb':
                        dba = 'Mongodb'
                        extras = 'The MERN stack (MongoDB, Express.js, React.js, Node.js) is a great option for full stack development.'
                    if dbc == 'localdb':
                        dba = 'Sqlite'
                        extras = None
                    if dbc == 'nodb':
                        dba = None
                        extras = None
                if platform == 'os':
                    langa = 'Python'
                    if dbc == 'hosteddb':
                        dba = 'MySQL'
                    if dbc == 'localdb':
                        dba = 'Sqlite'
                    if dbc == 'nodb':
                        dba = None
                    extras == None
            return render_template('results.html', language=langa, ide=idea, dba=dba, extras=extras)
        else:
            error = 'Please answer all questions'
            render_template('quiz.html', error = error)
    return render_template("quiz.html", user = user)













@app.route('/results')
def results(lang, ide, db, extras):
    user = getCurrentUser()

    return render_template('results.html')



















@app.route('/logout')
def logout():
    if session:
        session.popitem()
    return redirect(url_for('index'))

if __name__ == "__main__":
    app.run(debug=True)