from kuvaruutu import app
from flask import render_template, request, redirect, url_for, flash
from kuvaruutu import util, users
from kuvaruutu.forms import CommentForm, PostForm, RegistrationForm, LoginForm, DeleteForm
from werkzeug.datastructures import MultiDict


@app.route('/', methods=['get'])
def index():
    posts = util.get_all_posts() 
    comment_count = []
    images = []
    comments = []
    # Haetaan jokaisen viestin vastausten määrä
    for post in posts:
        id = post[0]
        # print('nyt haetaan viestin id', msg[0], 'vastausten maaraa')
        comments.append(util.get_comments_for_post_for_index(id))
        comment_count.append(len(util.get_comments_for_post(id)))
        images.append(util.get_image(id))
        
    # print('images listan pituus', len(images))
    return render_template('index.html', count=len(posts), posts=enumerate(posts), comment_count=comment_count, images=images, comments=enumerate(comments))


@app.route('/show/<int:id>')
def show(id):
    # TESTIKÄYTTÖ KUVILLE
    # Vaatii messages get_image muokkausta toimiakseen. 
    response = util.magnify_the_image(id)
    return response


@app.route('/new_post', methods=['get','post'])
def new_post():
    form = PostForm()
    if request.method == 'POST':
        print('post')
    if form.validate_on_submit():
        file = request.files['file']
        # print('routesissa saatu file', file)
        # print('ja sen type', type(file))
        title = request.form['title']
        content = request.form['content']
        if not file:
            return 'nothing uploaded', 400
        if util.send(title, content, file):
            return redirect('/')
        else:
            return render_template('error.html',message='Submitting the post failed for some reason.')
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
        #TODO Jos kommentin lähetys ei onnistu
    
@app.route('/profile', methods=['GET','POST'])
def profile():
    form = DeleteForm()
    if request.method == 'POST':
        post_id = request.form['post_id']
        util.delete_post(post_id)
 
    id = users.get_user_id()
    posts = util.get_posts_with_id(id)
    comments = util.get_comments_for_user(id)
    post_amount = len(posts)
    comment_amount = len(comments)
    images = []
    for msg in posts:
        id = msg[0]
        # print('nyt haetaan viestin id', msg[0], 'vastausten maaraa')
        images.append(util.get_image(id))

    return render_template('profile.html', title='Profile', posts=enumerate(posts), images=images, post_amount=post_amount, comments=comments, comment_amount=comment_amount, form=form)
    

@app.route('/posts/<int:id>', methods=['get','post'])
def posts(id):
    form = CommentForm()
    if form.validate_on_submit():
        # print('kommentoitiin.')
        content = request.form['content']
        if not util.send_comment(content, id):
            return render_template('error.html',message='Submitting the comment failed.')
    post = util.get_one_post(id)
    message_id = post[0][0]
    comments = util.get_comments_for_post(id)
    image = util.get_image(message_id)
    # print('imagen type', type(image))
    return render_template('posts.html', id=id, comments=comments, post=post, count=len(comments), image=image, form=form)

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
    # print('ja taas mennään')
    return render_template('register.html', title='Register', form=form)
