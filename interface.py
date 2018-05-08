"""
Database Model interface for the COMP249 Web Application assignment

@author: caitlin bell
"""


def position_list(db, limit=10):
    """Return a list of positions ordered by date
    db is a database connection
    return at most limit positions (default 10)

    Returns a list of tuples  (id, timestamp, owner, title, location, company, description)
    """
    cursor = db.cursor()
    sql = '''
    SELECT id, timestamp, owner, title, location, company, description 
    FROM positions 
    ORDER BY timestamp DESC
    LIMIT(?)
    '''
    cursor.execute(sql, (limit,))
    return cursor.fetchall()


def position_get(db, id):
    """Return the details of the position with the given id
    or None if there is no position with this id

    Returns a tuple (id, timestamp, owner, title, location, company, description)

    """
    cursor = db.cursor()
    sql = '''
    SELECT id, timestamp, owner, title, location, company, description
    FROM positions 
    WHERE id = (?)
    '''
    cursor.execute(sql, (id,))
    if cursor.rowcount is 0:
        return "None"
    else:
        return cursor.fetchone()


def position_add(db, usernick, title, location, company, description):
    """Add a new post to the database.
    The date of the post will be the current time and date.
    Only add the record if usernick matches an existing user

    Return True if the record was added, False if not."""
    cursor = db.cursor()
    sql = '''
       SELECT nick 
       FROM users
       '''
    add = '''
    INSERT INTO positions (owner, title, location, company, description) 
    VALUES (:owner, :title, :location, :company, :description) 
    '''
    cursor.execute(sql)
    userlist = [row[0] for row in cursor]

    if usernick not in userlist:
        return False
    else:
        cursor.execute(add, {'owner': usernick, 'title': title, 'location': location, 'company': company,
                             'description': description})
        db.commit()
        return True
