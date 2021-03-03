from app import app
from flask import render_template, request
from app.forms import UserInfoForm, PostForm


@app.route('/')
@app.route('/index')
def hello_world():
    
    context = {
        'title': "Kekembas Blog | HOME",
        'customer_name': 'Shoha',
        'customer_username': 'smtsuchi',
        
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
    return render_template('register.html', title = title, form = form)

@app.route('/createPost', methods=['GET','POST'])
def createPost():
    title = "Kekembas Blog | CREATE POST"
    post = PostForm()
    if request.method == 'POST' and post.validate():
        post_title = post.title.data
        content = post.content.data
        print(post_title, content)
    return render_template('create_post.html', title = title, post = post)