from . import bp as blog
from flask import request, redirect, url_for,jsonify, render_template
from app import db
from flask_login import login_required, current_user
from .forms import PostForm
from app.models import Post

@blog.route('/createPost', methods=['GET','POST'])
@login_required
def createPost():
    title = "Kekembas Blog | CREATE POST"
    post = PostForm()
    if request.method == 'POST' and post.validate():
        post_title = post.title.data
        image = post.image.data
        content = post.content.data
        user_id = 1
        # print(post_title, content)
        # create new post instance
        new_post = Post(post_title, image, content, user_id)
        # add new post instance to database
        db.session.add(new_post)
        # commit
        db.session.commit()
        # flash a message
        flash("You have successfully created a post!", 'success')
        # redirect back to create post
        return redirect(url_for('createPost'))
    return render_template('create_post.html', title = title, post = post)

@blog.route('/myposts')
# @login_required
def myPosts():
    title = "Kekembas Blog | MY POSTS"
    # posts = current_user.post
    posts = Post.query.all()
    return jsonify([p.to_dict() for p in posts]) #able to now make an API call to this url
    # return render_template('my_posts.html', title = title, posts = posts)

@blog.route('/myposts/<int:post_id>')
# @login_required
def post_detail(post_id):
    post = Post.query.get_or_404(post_id)
    title = f"Kekembas Blog | {post.title.upper()}"
    return jsonify(post.to_dict())
    # return render_template('post_detail.html', post = post, title = title)

@blog.route('/myposts/update/<int:post_id>', methods =['GET','POST'])
# @login_required
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

@blog.route('/myposts/delete/<int:post_id>', methods=['POST'])
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