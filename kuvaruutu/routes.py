from kuvaruutu import app
from flask import render_template, request, redirect, url_for, flash
from kuvaruutu import messages, users
from kuvaruutu.forms import CommentForm, PostForm, RegistrationForm, LoginForm
from werkzeug.security import generate_password_hash


@app.route('/', methods=['GET'])
def index():
    list = messages.get_list() 
    comment_count = []
    images = []
    # Haetaan jokaisen viestin vastausten määrä
    for msg in list:
        id = msg[3]
        # print('nyt haetaan viestin id', msg[3], 'vastausten maaraa')
        comment_count.append(len(messages.get_comments(id)))
        images.append(messages.get_image(id))
    print('images listan pituus', len(images))
    return render_template('index.html', count=len(list), messages=enumerate(list), comment_count=comment_count, images=images)

@app.route('/show/<int:id>')
def show(id):
    # TESTIKÄYTTÖ KUVILLE
    response = messages.get_image(id)
    return response


@app.route('/new_post', methods=['get','post'])
def new_post():
    form = PostForm()
    if request.method == 'POST':
        print('post')
    if form.validate_on_submit():
        file = request.files['file']
        print('routesissa saatu file', file)
        print('ja sen type', type(file))
        content = request.form['content']
        if not file:
            return 'nothing uploaded', 400
        if messages.send(content, file):
            return redirect('/')
        else:
            return render_template('error.html',message='Viestin lähetys ei onnistunut')
    return render_template('new_post.html', title='Make a New Post', form=form)

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
    return render_template('profile.html', title='Profilel')
    



@app.route('/posts/<int:id>', methods=['get','post'])
def posts(id):
    form = CommentForm()
    if form.validate_on_submit():
        print('kommentoitiin.')
        content = request.form['content']
        if not messages.send_comment(content, id):
            return render_template('error.html',message='Viestin lähetys ei onnistunut')
    og_message = messages.get_one_comment(id)
    message_id = og_message[0][3]
    posts = messages.get_comments(id)
    image = messages.get_image(message_id)
    print('imagen type', type(image))
    return render_template('posts.html', id=id, comments=posts, og_message=og_message, count=len(posts), image=image, form=form)

@app.route('/send', methods=['POST'])
def send():
    print('sendissä')
    #TODO tiedoston nimen ja koon tarkastaminen. 
    file = request.files['file']
    print('routesissa saatu file', file)
    print('ja sen type', type(file))
    content = request.form['content']
    if not file:
        return 'nothing uploaded', 400

    if messages.send(content, file):
        return redirect('/')
    else:
        return render_template('error.html',message='Viestin lähetys ei onnistunut')

@app.route('/login', methods=['get','post'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        username = request.form['username']
        password = request.form['password']
        if users.login(username,password):
            flash(f'Welcome {form.username.data}', 'success')
            return redirect('/')
        else:
            return render_template('error.html',message='Väärä tunnus tai salasana')

    return render_template('login.html', title='Login', form=form)

@app.route('/logout')
def logout():
    users.logout()
    return redirect('/')

@app.route('/register', methods=['get','post'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        # username = request.form['username']
        # password = request.form['password']
        # print(form.username.data, request.form['username'])
        if users.register(username,password):
            flash(f'Account created for {form.username.data}', 'success')
            return redirect('/')
        else:
            return render_template('error.html',message='Rekisteröinti ei onnistunut')
    print('ja taas mennään')
    return render_template('register.html', title='Register', form=form)
