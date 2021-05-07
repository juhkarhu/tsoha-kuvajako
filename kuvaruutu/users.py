from kuvaruutu import db, util
from flask import session
from werkzeug.security import check_password_hash, generate_password_hash
import os

def login(username,password):
    sql = 'SELECT password, id, username, banned FROM users WHERE username=:username'
    result = db.session.execute(sql, {'username':username})
    user = result.fetchone()
    if user == None:
        return False, 'none'
    else:
        if check_password_hash(user[0],password) and user[3] == 0:
            session['username'] = user[2]
            session['user_id'] = user[1]
            session['admin'] = is_admin()
            return True, 'none'
        elif user[3] == 1:
            return False, 'banned'
        else:
            return False, 'none'

def logout():
    del session['user_id']

def register(username,password):
    hash_value = generate_password_hash(password)
    try:
        sql = 'INSERT INTO users (username,password) VALUES (:username,:password)'
        db.session.execute(sql, {'username':username,'password':hash_value})
        db.session.commit()
    except:
        return False
    return login(username,password)

def get_user_id():
    return session.get('user_id',0)

def is_admin():
    status = util.is_admin_query()
    return status