from kuvaruutu import db
from flask import session
from werkzeug.security import check_password_hash, generate_password_hash
import os

def login(username,password):
    sql = 'SELECT password, id FROM users WHERE username=:username'
    result = db.session.execute(sql, {'username':username})
    user = result.fetchone()
    if user == None:
        return False
    else:
        if check_password_hash(user[0],password):
            session['user_id'] = user[1]
            # session['csrf_token'] = os.urandom(16).hex()
            return True
        else:
            return False

def logout():
    del session['user_id']

def register(username,password):
    hash_value = generate_password_hash(password)
    print('1')
    try:
        print('2')
        sql = 'INSERT INTO users (username,password) VALUES (:username,:password)'
        print('3')
        db.session.execute(sql, {'username':username,'password':hash_value})
        print('4')
        db.session.commit()
    except:
        return False
    return login(username,password)

def get_user_id():
    return session.get('user_id',0)
