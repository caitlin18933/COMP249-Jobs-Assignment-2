"""
@author: Caitlin Bell
"""
import uuid
import database
from bottle import response, request
# this variable MUST be used as the name for the cookie used by this application
COOKIE_NAME = 'sessionid'


def check_login(db, usernick, password):
    """returns True if password matches stored"""
    cursor = db.cursor()
    sql = '''
        SELECT nick, password
        FROM users 
        WHERE nick = (?) AND password = (?)
        '''
    cursor.execute(sql, (usernick, database.password_hash(password)))
    result = cursor.fetchone()
    if result is None:
        return False
    else:
        return True


def generate_session(db, usernick):
    """create a new session and add a cookie to the response object (bottle.response)
    user must be a valid user in the database, if not, return None
    There should only be one session per user at any time, if there
    is already a session active, use the existing sessionid in the cookie
    """
    cursor = db.cursor()
    getuser = 'SELECT nick FROM users'
    cursor.execute(getuser)
    userlist = [row[0] for row in cursor]
    cursor.close()
    if usernick not in userlist:
        return None
    else:
        cursor = db.cursor()
        checksession = 'SELECT sessionid FROM sessions WHERE usernick = (?)'
        cursor.execute(checksession, (usernick,))
        currentsession = cursor.fetchone()

        if currentsession is not None:
            sessionid = currentsession[0]
        else:
            sessionid = uuid.uuid4().hex
            sql = 'INSERT INTO sessions (usernick, sessionid) VALUES (?, ?)'
            cursor.execute(sql, (usernick, sessionid))
            db.commit()
        response.set_cookie(COOKIE_NAME, sessionid)


def delete_session(db, usernick):
    """remove all session table entries for this user"""
    cursor = db.cursor()
    sql = 'DELETE FROM sessions WHERE usernick = (?)'
    cursor.execute(sql, (usernick,))
    db.commit()


def session_user(db):
    """try to
    retrieve the user from the sessions table
    return usernick or None if no valid session is present"""
    cursor = db.cursor()
    sql = 'SELECT usernick FROM sessions WHERE sessionid = ?'
    sessionid = request.get_cookie(COOKIE_NAME)
    if sessionid is None:
        return None
    cursor.execute(sql, (sessionid,))
    name = cursor.fetchone()
    if name is None:
        return None
    else:
        return name[0]
