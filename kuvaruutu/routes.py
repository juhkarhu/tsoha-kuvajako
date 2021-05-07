from kuvaruutu import app
from flask import render_template, request, redirect, url_for, flash

from kuvaruutu import util, users
from kuvaruutu.forms import CommentForm, PostForm, RegistrationForm, LoginForm, DeleteForm, AdminForm, SearchForm
from werkzeug.datastructures import MultiDict


@app.route('/', methods=['get', 'post'])
def index():
    '''
    Serves the frontpage. Displays all the post and 3 most recent comment for each post.
    Images are in a separate table and are fetched to each post independently.
    '''
    posts = util.get_all_posts()
    comment_count, images, comments = util.get_images_and_comments(posts)

    return render_template('index.html', count=len(posts), posts=enumerate(posts), comment_count=comment_count, images=images, comments=comments)

@app.route('/search', methods=['get', 'post'])
def search():
    '''
    Users can search for posts using keywords.
    '''
    form = SearchForm()
    if form.validate_on_submit():
        keyword = '%{}%'.format(request.form['query'])
        posts = util.search_all_posts(keyword)
    else:
        posts = util.get_all_posts() 
    comment_count, images, comments = util.get_images_and_comments(posts)

    return render_template('search.html', form=form, count=len(posts), posts=enumerate(posts), comment_count=comment_count, images=images, comments=comments)

@app.route('/admin', methods=['GET', 'POST'])
def admin():
    '''
    This is pretty similar to index and profile pages.
    The exception is, that every post and every comment gets loaded and can be deleted.
    '''
    form = AdminForm()
    if users.is_admin():
        if request.method == 'POST':
            if request.form['del_type'] == 'post':
                post_id = request.form['post_id']
                util.delete_post(post_id)
            if request.form['del_type'] == 'comment':
                comment_id = request.form['comment_id']
                util.delete_comment(comment_id)
            if request.form['del_type'] == 'user':
                user_id = request.form['user_id']
                print(user_id)
                util.ban_user(user_id)
        
        id = users.get_user_id()
        posts = util.get_all_posts_as_admin()
        comments = []
        images = []
        comment_count = []
        for post in posts:
            id = post[0]
            comments.append(util.get_comments_for_post_for_index_as_admin(id))
            comment_count.append(len(util.get_comments_for_post(id)))
            images.append(util.get_image(id))
        user_list = util.get_all_users()
        return render_template('admin.html', form=form, count=len(posts), posts=enumerate(posts), comment_count=comment_count, images=images, comments=comments, users=user_list)
    else:
        return redirect('/')


@app.route('/profile', methods=['GET','POST'])
def profile():
    '''
    Shows all the users posts and comments.
    '''
    form = DeleteForm()
    if request.method == 'POST':
        if request.form['del_type'] == 'post':
            post_id = request.form['post_id']
            util.delete_post(post_id)
            return redirect('/profile')
        if request.form['del_type'] == 'comment':
            comment_id = request.form['comment_id']
            util.delete_comment(comment_id)

    id = users.get_user_id()
    posts = util.get_posts_for_profile(id)
    comments = util.get_comments_for_user(id)
    post_amount = len(posts)
    comment_amount = len(comments)
    images = util.get_images_for_posts(posts)
    return render_template('profile.html', title='Profile', posts=enumerate(posts), images=images, post_amount=post_amount, comments=comments, comment_amount=comment_amount, form=form)



@app.route('/new_post', methods=['get','post'])
def new_post():
    '''
    Form for adding a new post.
    Input file is mandatory.
    '''
    form = PostForm()
    if form.validate_on_submit():
        file = request.files['file']
        title = request.form['title']
        content = request.form['content']
        if not file:
            return 'nothing uploaded', 400
        if util.send(title, content, file):
            return redirect('/')
        else:
            return render_template('error.html',message='Submitting the post failed for some reason.')
    return render_template('new_post.html', title='Make a New Post', form=form)



@app.route('/posts/<int:id>', methods=['get','post'])
def posts(id):
    form = CommentForm()
    if form.validate_on_submit():
        content = request.form['content']
        if not util.send_comment(content, id):
            return render_template('error.html',message='Submitting the comment failed.')
        return redirect('/posts/' + str(id))
    post = util.get_one_post(id)
    message_id = post[0][0]
    comments = util.get_comments_for_post(id)
    image = util.get_image(message_id)
    return render_template('posts.html', id=id, comments=comments, post=post, count=len(comments), image=image, form=form)

@app.route('/login', methods=['get','post'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        username = request.form['username']
        password = request.form['password']
        (okay, banned) = users.login(username,password)
        if okay:
            flash(f'Welcome {form.username.data}', 'success')
            return redirect('/')
        elif (banned == 'banned'):
            return render_template('error.html',message='Your account has been suspended by admins.')
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
        if users.register(username,password):
            flash(f'Account created for {form.username.data}', 'success')
            return redirect('/')
        else:
            return render_template('error.html',message='Rekisteröinti ei onnistunut')
    return render_template('register.html', title='Register', form=form)
