from app import app
from flask import render_template, request, redirect
import messages, users


@app.route("/", methods=['GET'])
def index():
    print('1')
    list = messages.get_list() 
    print('2')
    comment_count = []
    # Haetaan jokaisen viestin vastausten määrä
    for msg in list:
        print('viesti:', msg)
        # print('nyt haetaan viestin id', msg[3], 'vastausten maaraa')
        comment_count.append(len(messages.get_comments(msg[3])))
    print('3')
    return render_template('index.html', count=len(list), messages=enumerate(list), comment_count=comment_count)

@app.route('/show/<int:id>')
def show(id):
    # TESTIKÄYTTÖ KUVILLE
    response = messages.get_image(id)
    return response


@app.route('/new_post')
def new_post():
    return render_template('new_post.html')

@app.route('/comment', methods=['POST'])
def comment():
    id = request.form['id']
    content = request.form['content']
    # print('saatu id', id, 'ja content', content)
    if messages.send_comment(content, id):
        return redirect('/comments/' + id)
    else:
        pass
        #TODO Jos vastauksen lähetys ei onnistu
    
@app.route('/profile')
def profile():
    pass
    



@app.route('/comments/<int:id>')
def comments(id):
    og_message = messages.get_one_comment(id)
    message_id = og_message[0][3]
    comments = messages.get_comments(id)
    image = messages.get_image(message_id)
    return render_template('comments.html', id=id, comments=comments, og_message=og_message, count=len(comments), image=image)

@app.route('/send', methods=['POST'])
def send():
    #TODO tiedoston nimen ja koon tarkastaminen. 
    file = request.files['file']
    content = request.form['content']
    if not file:
        return 'nothing uploaded', 400

    if messages.send(content, file):
        return redirect('/')
    else:
        return render_template('error.html',message='Viestin lähetys ei onnistunut')

@app.route('/login', methods=['get','post'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if users.login(username,password):
            return redirect('/')
        else:
            return render_template('error.html',message='Väärä tunnus tai salasana')

@app.route('/logout')
def logout():
    users.logout()
    return redirect('/')

@app.route('/register', methods=['get','post'])
def register():
    if request.method == 'GET':
        return render_template('register.html')
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if users.register(username,password):
            return redirect('/')
        else:
            return render_template('error.html',message='Rekisteröinti ei onnistunut')
