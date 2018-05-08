__author__ = 'Caitlin Bell 45217734'

from bottle import Bottle, template, static_file, request, redirect
import interface, users
app = Bottle()


@app.route('/')
def index(db):
    poslist = interface.position_list(db, 10)
    name = users.session_user(db)

    info = {
        'title': 'The Chalkboard',
        'message': 'Welcome to Jobs!',
        'name': name
        }

    return template('index', info, jobs=poslist)


@app.route('/login', method='POST')
def login(db):
    username = request.forms.get('nick')
    password = request.forms.get('password')
    if users.check_login(db, username, password):
        users.generate_session(db, username)
        message = str("Logged in as " + username)
        redirect('/')
        return message
    else:
        return template('failedlogin')


@app.route('/logout', method='POST')
def logout(db):
    name = users.session_user(db)
    users.delete_session(db, name)
    redirect('/')


@app.route('/post', method='POST')
def post(db):
    name = users.session_user(db)
    title = request.forms.get('title')
    location = request.forms.get('location')
    company = request.forms.get('company')
    description = request.forms.get('description')

    interface.position_add(db, name, title, location, company, description)
    redirect('/')


@app.route('/about')
def about(db):
    name = users.session_user(db)
    info = {
        'title': 'The Chalkboard',
        'name': name
    }

    return template('about', info)


@app.route('/positions/<id>')
def position(db, id):
    joblist = list(interface.position_get(db, id))
    name = users.session_user(db)
    info = {
        'title': 'The Chalkboard',
        'message': 'Welcome to Jobs!',
        'jobtitle': joblist[3],
        'timestamp': joblist[1],
        'company': joblist[5],
        'location': joblist[4],
        'description': joblist[6],
        'owner': joblist[2],
        'name': name


    }

    return template('positions', info)


@app.route('/static/<filename:path>')
def static(filename):
    return static_file(filename=filename, root='static')


if __name__ == '__main__':

    from bottle.ext import sqlite
    from database import DATABASE_NAME
    # install the database plugin
    app.install(sqlite.Plugin(dbfile=DATABASE_NAME))
    app.run(debug=True, port=8010)
