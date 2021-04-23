from kuvaruutu import db
from flask import make_response
from kuvaruutu import users
from werkzeug.utils import secure_filename
from base64 import b64encode
from PIL import Image



SIZE = 256, 256
 

def get_all_posts(): 
    sql = 'SELECT P.id, P.title, P.content, U.username, P.sent_at, P.visible FROM posts P, users U WHERE P.user_id=U.id ORDER BY P.sent_at DESC'
    result = db.session.execute(sql)
    return result.fetchall()

def get_posts_with_id(id):
    sql = 'SELECT P.id, P.title, P.content, U.username, P.sent_at, P.visible FROM posts P, users U WHERE P.user_id=U.id AND U.id=:id ORDER BY P.sent_at DESC'
    result = db.session.execute(sql, {'id':id})
    return result.fetchall()

def send(title, content, file):
    #TODO Kuvan muokkaus: koko, reso

    filename = secure_filename(file.filename)
    data=file.read()
    #print('lahetetyn kuvan data muoto', type(data))
    
    user_id = users.get_user_id()
    if user_id == 0:
        return False

    sql = 'INSERT INTO posts (title, content, user_id, sent_at) VALUES (:title, :content, :user_id, NOW()) RETURNING id'
    result = db.session.execute(sql, {'title':title, 'content':content, 'user_id':user_id})
    message_id = result.fetchone()[0]
    #print('saatu post id', message_id)
    db.session.commit()

    sql = 'INSERT INTO images (name, message_id, data) VALUES (:name, :message_id, :data)'
    db.session.execute(sql, {'name':filename, 'message_id':message_id, 'data':data})
    db.session.commit()
    return True

def send_comment(content, comment_id):
    user_id = users.get_user_id()
    if user_id == 0:
        return False
    sql = 'INSERT INTO comments (content, comment_id, user_id, sent_at) ' \
          'VALUES (:content, :comment_id, :user_id, NOW())'
    db.session.execute(sql, {'content':content, 'comment_id':comment_id, 'user_id':user_id})
    db.session.commit()
    return True

def get_comments_for_post(id):
    sql = 'SELECT C.content, U.username, C.sent_at ' \
        'FROM posts P, comments C, users U WHERE P.id=:id AND P.id=C.comment_id AND ' \
        'U.id=C.user_id ORDER BY C.id'
    result = db.session.execute(sql, {'id':id})
    comments = result.fetchall()
    return comments

def get_comments_for_user(id):
    sql = 'SELECT C.content, U.username, C.sent_at, C.comment_id ' \
        'FROM posts P, comments C, users U WHERE U.id=:id AND P.id=C.comment_id AND ' \
        'U.id=C.user_id ORDER BY C.id'
    result = db.session.execute(sql, {'id':id})
    comments = result.fetchall()
    return comments

def get_one_comment(id):
    sql = 'SELECT P.content, U.username, P.sent_at, P.id FROM posts P, users U WHERE P.id=:id'
    result = db.session.execute(sql, {'id':id})
    og_comment = result.fetchall()
    return og_comment

def get_image(id):
    #print('saatu id', id)
    sql = 'SELECT data FROM images WHERE id=:id'
    result = db.session.execute(sql, {'id':id})
    data = result.fetchone()[0]
    image = b64encode(data).decode('utf-8')
    sql = 'SELECT name, id FROM images WHERE id=:id'
    result = db.session.execute(sql, {'id':id})
    filename = result.fetchone()[0]
    return (image, filename)

    # # Tämä toimii ja kirjoittaa kuvan tiedostoon mutta lähetää class intin eteenpäin.
    # with open('kuva.jpg', 'wb') as q:
    #     kuva = q.write(data)
    #     # fp = io.StringIO()
    #     # kuva.sa
    #     # q.write(data)
    # return kuva

    # # Tämä toimii jos käyttää /show/:id menetelmää
    # response = make_response(bytes(data))
    # response.headers.set('Content-Type','image/jpeg')
    # print('response', response)
    # return response
    
def magnify_the_image(id):
    sql = 'SELECT data FROM images WHERE id=:id'
    result = db.session.execute(sql, {'id':id})
    data = result.fetchone()[0]
    response = make_response(bytes(data))
    response.headers.set('Content-Type','image/jpeg')
    print('response', response)
    return response