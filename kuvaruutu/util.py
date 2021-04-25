from kuvaruutu import db
from flask import make_response
from kuvaruutu import users
from werkzeug.utils import secure_filename
from base64 import b64encode
from PIL import Image
import io


def get_all_posts(): 
    sql = 'SELECT P.id, P.title, P.content, U.username, P.sent_at, P.visible FROM posts P, users U WHERE P.user_id=U.id AND P.visible=1 ORDER BY P.sent_at DESC'
    result = db.session.execute(sql)
    return result.fetchall()

def get_all_posts_as_admin(): 
    sql = 'SELECT P.id, P.title, P.content, U.username, P.sent_at, P.visible FROM posts P, users U WHERE P.user_id=U.id ORDER BY P.sent_at DESC'
    result = db.session.execute(sql)
    return result.fetchall()

def search_all_posts(keyword): 
    sql = 'SELECT DISTINCT ON (P.sent_at) P.id, P.title, P.content, U.username, P.sent_at, P.visible FROM posts P, users U WHERE P.user_id=U.id AND P.visible=1 AND P.title ILIKE :keyword OR P.content ILIKE :keyword GROUP BY P.id, U.username'
    result = db.session.execute(sql, {'keyword':keyword})
    return result.fetchall()

def get_posts_for_profile(id):
    sql = 'SELECT P.id, P.title, P.content, U.username, P.sent_at, P.visible, P.user_id FROM posts P, users U WHERE U.id=:id AND P.user_id=U.id ORDER BY P.sent_at DESC'
    result = db.session.execute(sql, {'id':id})
    return result.fetchall()

def get_one_post(id):
    sql = 'SELECT P.id, P.title, P.content, U.username, P.sent_at, P.user_id FROM posts P, users U WHERE P.id=:id and P.user_id=U.id'
    result = db.session.execute(sql, {'id':id})
    post = result.fetchall()
    return post

def send(title, content, file):
    if not is_banned():
        filename = secure_filename(file.filename)
        data = resize_image(file)
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

def send_comment(content, post_id):
    user_id = users.get_user_id()
    if user_id == 0:
        return False
    sql = 'INSERT INTO comments (content, post_id, user_id, sent_at) ' \
          'VALUES (:content, :post_id, :user_id, NOW())'
    db.session.execute(sql, {'content':content, 'post_id':post_id, 'user_id':user_id})
    db.session.commit()
    return True

def is_admin_query():
    admin_query = 'SELECT admin FROM users WHERE id=:id'
    result = db.session.execute(admin_query, {'id':users.get_user_id()})
    result = result.fetchone()[0]
    if (result == 1):
        return True
    return False

def is_banned():
    sql = 'SELECT banned FROM users WHERE id=:id'
    result = db.session.execute(sql, {'id':users.get_user_id()})
    result = result.fetchone()[0]
    if (result == 1):
        return True
    return False

def admin_search(keyword):
    post_sql = 'SELECT P.id, P.title, P.content FROM posts P WHERE (content LIKE :keyword or title LIKE :keyword)'
    post_query = db.session.execute(post_sql, {'keyword':keyword})
    posts = post_query.fetchall()
    # print('admin_search.posts', posts)

    comment_sql = 'SELECT C.id, C.content, C.post_id, C.user_id FROM comments C, users U WHERE U.username LIKE :keyword AND C.user_id=U.id'
    comment_query = db.session.execute(comment_sql, {'keyword':keyword})
    comments = comment_query.fetchall()
    # print('admin_search.comments', comments)

    user_sql = 'SELECT U.username, U.id FROM users U WHERE U.username LIKE :keyword'
    user_query = db.session.execute(user_sql, {'keyword':keyword})
    users = user_query.fetchall()
    # print('admin_search.users', users)

    return users, posts, comments


def admin_search_for_user(keyword):
    sql = 'SELECT id, username FROM users WHERE username LIKE :keyword'
    result = db.session.execute(sql, {'keyword':keyword})
    result = result.fetchone()
    # print('admin yhdelle tulos:', result)
    return result

def get_all_users():
    sql = 'SELECT id, username, banned FROM users'
    result = db.session.execute(sql)
    users = result.fetchall()
    return users

def delete_post(id):
    admin_result = is_admin_query()
    sql = 'SELECT visible FROM posts WHERE id=:id'
    result = db.session.execute(sql, {'id':id})
    ans = result.fetchone()[0]
    print(ans)
    # sql = ''

    if (ans == 0 and admin_result):
        print('tehtiin näkyväksi')
        sql = 'UPDATE posts SET visible=1 WHERE id=:id'
    else:
        print('piilotettiin')
        sql = 'UPDATE posts SET visible=0 WHERE id=:id'
    # sql = 'UPDATE posts SET visible=0 WHERE id=:id'
    db.session.execute(sql, {'id':id})
    db.session.commit()

def delete_comment(id):
    admin_result = is_admin_query()
    sql = 'SELECT visible FROM comments WHERE id=:id'
    result = db.session.execute(sql, {'id':id})
    ans = result.fetchone()[0]
    print('comment ans', ans)
    if (ans == 0 and admin_result):
        print('kommentti tehtiin näkyväksi')
        sql = 'UPDATE comments SET visible=1 WHERE id=:id'
    else:
        print('kommentti piilotettiin')
        sql = 'UPDATE comments SET visible=0 WHERE id=:id'

    db.session.execute(sql, {'id':id})
    db.session.commit()

def ban_user(id):
    admin_result = is_admin_query()
    if admin_result:
        sql = 'UPDATE users SET banned=1 WHERE id=:id'
        db.session.execute(sql, {'id':id})
        db.session.commit()



def get_comments_for_post(id):
    sql = 'SELECT C.content, U.username, C.sent_at ' \
        'FROM posts P, comments C, users U WHERE P.id=:id AND P.id=C.post_id AND ' \
        'U.id=C.user_id AND C.visible=1 ORDER BY C.id'
    result = db.session.execute(sql, {'id':id})
    comments = result.fetchall()
    return comments

def get_comments_for_post_as_admin(id):
    sql = 'SELECT C.content, U.username, C.sent_at ' \
        'FROM posts P, comments C, users U WHERE P.id=:id AND P.id=C.post_id AND ' \
        'U.id=C.user_id ORDER BY C.id'
    result = db.session.execute(sql, {'id':id})
    comments = result.fetchall()
    return comments

def get_comments_for_post_for_index(id):
    sql = 'SELECT C.content, U.username, C.sent_at, C.id ' \
        'FROM posts P, comments C, users U WHERE P.id=:id AND P.id=C.post_id AND C.visible=1 AND ' \
        'U.id=C.user_id ORDER BY C.id LIMIT 3'
    result = db.session.execute(sql, {'id':id})
    comments = result.fetchall()
    return comments

def get_comments_for_post_for_index_as_admin(id):
    sql = 'SELECT C.content, U.username, C.sent_at, C.id, C.visible ' \
        'FROM posts P, comments C, users U WHERE P.id=:id AND P.id=C.post_id AND ' \
        'U.id=C.user_id ORDER BY C.id LIMIT 3'
    result = db.session.execute(sql, {'id':id})
    comments = result.fetchall()
    return comments

def get_comments_for_user(id):
    sql = 'SELECT C.content, U.username, C.sent_at, C.post_id, C.post_id, C.visible ' \
        'FROM posts P, comments C, users U WHERE C.visible=1 AND U.id=:id AND P.id=C.post_id AND ' \
        'U.id=C.user_id ORDER BY C.id'
    result = db.session.execute(sql, {'id':id})
    comments = result.fetchall()
    return comments



def get_image(id):
    # print('saatu id', id)
    sql = 'SELECT data FROM images WHERE id=:id'
    result = db.session.execute(sql, {'id':id})
    data = result.fetchone()[0]
    image = b64encode(data).decode('utf-8')
    sql = 'SELECT name, id FROM images WHERE id=:id'
    result = db.session.execute(sql, {'id':id})
    filename = result.fetchone()[0]
    return (image, filename)


def magnify_the_image(id):
    sql = 'SELECT data FROM images WHERE id=:id'
    result = db.session.execute(sql, {'id':id})
    data = result.fetchone()[0]
    response = make_response(bytes(data))
    response.headers.set('Content-Type','image/jpeg')
    # print('response', response)
    return response


def resize_image(file):
    '''
    Resizes the images. 
    '''
    basewidth = 400
    img = Image.open(file)
    wpercent = (basewidth/float(img.size[0]))
    hsize = int((float(img.size[1])*float(wpercent)))
    img = img.resize((basewidth,hsize), Image.ANTIALIAS)
    img_byte_arr = io.BytesIO()
    img.save(img_byte_arr, format='PNG')
    img_byte_arr = img_byte_arr.getvalue()
    return img_byte_arr


def get_images_for_posts(posts):
    # print('saatu posts', posts)
    images = []
    if len(posts) > 0:
        for post in posts:
            id = post[0]
            images.append(get_image(id))
    return images