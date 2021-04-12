from kuvaruutu import app
from flask import render_template, request, redirect, url_for, flash
from kuvaruutu import util, users
from kuvaruutu.forms import CommentForm, PostForm, RegistrationForm, LoginForm
from werkzeug.security import generate_password_hash


@app.route('/', methods=['get'])
def index():
    list = util.get_all_posts() 
    comment_count = []
    images = []
    # Haetaan jokaisen viestin vastausten määrä
    for msg in list:
        id = msg[3]
        # print('nyt haetaan viestin id', msg[3], 'vastausten maaraa')
        comment_count.append(len(util.get_comments_for_post(id)))
        images.append(util.get_image(id))
    print('images listan pituus', len(images))
    return render_template('index.html', count=len(list), messages=enumerate(list), comment_count=comment_count, images=images)

@app.route('/show/<int:id>')
def show(id):
    # TESTIKÄYTTÖ KUVILLE
    # Vaatii util get_image muokkausta toimiakseen. 
    response = util.get_image(id)
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
        if util.send(content, file):
            return redirect('/')
        else:
            return render_template('error.html',message='Viestin lähetys ei onnistunut')
    return render_template('new_post.html', title='Make a New Post', form=form)

@app.route('/comment', methods=['post'])
def comment():
    id = request.form['id']
    content = request.form['content']
    # print('saatu id', id, 'ja content', content)
    if util.send_comment(content, id):
        return redirect('/comments/' + id)
    else:
        pass
        #TODO Jos vastauksen lähetys ei onnistu
    
@app.route('/profile')
def profile():
    id = users.get_user_id()
    msgs = util.get_posts_with_id(id)


    return render_template('profile.html', title='Profilel', msgs=msgs)
    



@app.route('/posts/<int:id>', methods=['get','post'])
def posts(id):
    form = CommentForm()
    if form.validate_on_submit():
        print('kommentoitiin.')
        content = request.form['content']
        if not util.send_comment(content, id):
            return render_template('error.html',message='Viestin lähetys ei onnistunut')
    og_message = util.get_one_comment(id)
    message_id = og_message[0][3]
    comments = util.get_comments_for_post(id)
    image = util.get_image(message_id)
    print('imagen type', type(image))
    return render_template('posts.html', id=id, comments=comments, og_message=og_message, count=len(comments), image=image, form=form)

@app.route('/send', methods=['post'])
def send():
    print('sendissä')
    #TODO tiedoston nimen ja koon tarkastaminen. 
    file = request.files['file']
    print('routesissa saatu file', file)
    print('ja sen type', type(file))
    content = request.form['content']
    if not file:
        return 'nothing uploaded', 400

    if util.send(content, file):
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
