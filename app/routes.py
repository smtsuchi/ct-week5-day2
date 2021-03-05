from app import app, db, mail, Message
from flask import render_template, request, flash, redirect, url_for
from app.forms import UserInfoForm, PostForm, LoginForm
from app.models import User, Post
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import check_password_hash


@app.route('/')
@app.route('/index')
def hello_world():
    
    context = {
        'title': "Kekembas Blog | HOME",
        'posts': Post.query.all() #order_by(... .dec())
        
    }
    return render_template('index.html', **context)

@app.route('/register', methods=['GET','POST'])
def register():
    title = 'Kekembas Blog | REGISTER'
    form = UserInfoForm()
    if request.method == 'POST' and form.validate():
        username = form.username.data
        email = form.email.data
        password = form.password.data
        print(username, email, password)

        #create a new instance of user
        new_user = User(username, email, password)
        #add new instance to database
        db.session.add(new_user)
        #commit database
        db.session.commit()

        #send email to new user
        msg = Message(f'Welcome, {username}', [email])
        msg.body = 'Thank you for signing up to the Kekembas Blog, I hope you enjoy our app!'
        msg.html = '<p> Thank you so much for signing up for the Kekembas blog . I hopt you enjoy our app!</p>'

        mail.send(msg)

        flash("You have succesfully sign up!", "success")
        return redirect(url_for('hello_world'))

    return render_template('register.html', title = title, form = form)

@app.route('/createPost', methods=['GET','POST'])
@login_required
def createPost():
    title = "Kekembas Blog | CREATE POST"
    post = PostForm()
    if request.method == 'POST' and post.validate():
        post_title = post.title.data
        content = post.content.data
        user_id = current_user.id
        # print(post_title, content)
        # create new post instance
        new_post = Post(post_title, content, user_id)
        # add new post instance to database
        db.session.add(new_post)
        # commit
        db.session.commit()
        # flash a message
        flash("You have successfully created a post!", 'success')
        # redirect back to create post
        return redirect(url_for('createPost'))
    return render_template('create_post.html', title = title, post = post)


@app.route('/login', methods=['GET', 'POST'])
def login():
    title = "Kekembas Blog | LOGIN"
    form = LoginForm()
    if request.method == 'POST' and form.validate():
        username = form.username.data
        password = form.password.data

        user = User.query.filter_by(username=username).first()

        if user is None or not check_password_hash(user.password, password):
            flash("Incorrect Email/Password. Please try again", 'danger')
            return redirect(url_for('login'))

        login_user(user, remember=form.remember_me.data)
        flash("You have successfully logged in!", 'success')
        next_page = request.args.get('next')
        if next_page:
            return redirect(url_for(next_page.lstrip('/')))
        return redirect(url_for('hello_world'))

    return render_template('login.html', title = title, form = form)

@app.route('/logout')
def logout():
    logout_user()
    flash('You have succesfully logged out', 'primary')
    return redirect(url_for('hello_world'))

@app.route('/myinfo')
@login_required
def myInfo():
    title = 'Kekembas Blog | MY INFO'
    return render_template('my_info.html', title = title)

@app.route('/myposts')
@login_required
def myPosts():
    title = "Kekembas Blog | MY POSTS"
    posts = current_user.post
    return render_template('my_posts.html', title = title, posts = posts)

@app.route('/myposts/<int:post_id>')
@login_required
def post_detail(post_id):
    post = Post.query.get_or_404(post_id)
    title = f"Kekembas Blog | {post.title.upper()}"
    return render_template('post_detail.html', post = post, title = title)

@app.route('/myposts/update/<int:post_id>', methods =['GET','POST'])
@login_required
def post_update(post_id):
    post = Post.query.get_or_404(post_id)
    update_form = PostForm()
    if post.author.id != current_user.id:
        flash("You cannot update another user's post", "danger")
        return redirect(url_for('myPosts'))
    if request.method == "POST" and update_form.validate():
        post_title = update_form.title.data
        post_content = update_form.content.data

        post.title = post_title
        post.content = post_content

        db.session.commit()
        flash("Your post has been updated.", "info")
        return redirect(url_for('post_detail', post_id=post.id))

    return render_template('post_update.html', form = update_form, post=post)

@app.route('/myposts/delete/<int:post_id>', methods=['POST'])
@login_required
def post_delete(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author.id != current_user.id:
        flash("You cannot update another user's post", "danger")
        return redirect(url_for('myPosts'))
    db.session.delete(post)
    db.session.commit()
    flash("This entry has been deleted", 'info')
    return redirect(url_for('hello_world'))