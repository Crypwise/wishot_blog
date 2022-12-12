from flask import Blueprint, request, flash, redirect, render_template, url_for, abort
from flask_login import current_user, login_required
from wizapp import db
from wizapp.models import Post, Comment
from wizapp.posts.forms import postForm
from wizapp.users.utils import blog_image

posts = Blueprint('posts', __name__)


@posts.route("/post_details-<int:post_id>", methods=["POST", "GET"])
def post_details(post_id):
    post = Post.query.get_or_404(post_id)
    comments = Comment.query.filter_by(post_id=post.id).all()

    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        message = request.form.get('message')
        comment = Comment(name=name, email=email, message=message, post_id=post.id)
        db.session.add(comment)
        post.comments += 1
        flash('Your comment has been submitted', 'success')
        db.session.commit()
        return redirect(request.url)

    return render_template('post-details.html', title=post.title, post=post, comments=comments)


@posts.route('/post-new', methods=['GET', 'POST'])
@login_required
def new_post():
    form = postForm()
    if form.validate_on_submit():
        if form.image_post.data:
            image_file = blog_image(form.image_post.data)
            image_pic = image_file
            title = form.title.data
            content = form.content.data
            categories = form.categories.data
            author = current_user
            post = Post(title=title, content=content, image_pic=image_pic, categories=categories, author=author)
            db.session.add(post)
            db.session.commit()
            flash('Post created', 'success')
            return redirect(url_for('main.blog'))
    return render_template('Admin/create_post.html', legend='New_Post', form=form)


@posts.route('/post-<int:post_id>-update', methods=['POST', 'GET'])
@login_required
def update_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    form = postForm()
    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data
        post.image_pic = blog_image(form.image_post.data)
        db.session.commit()
        flash("Your Post Has Been Updated!", "success")
        return redirect(url_for('posts.post_details', post_id=post.id))
    elif request.method == 'GET':
        form.title.data = post.title
        form.content.data = post.content

    return render_template('Admin/create_post.html', title='Update Post', legend='update post', form=form)


@posts.route('/post-<int:post_id>-delete', methods=['POST'])
@login_required
def delete_post(post_id):
    try:
        if current_user:
            post = Post.query.filter(Post.id == post_id).delete()
            comment = Comment.query.filter(Comment.post_id == post_id).delete()
            db.session.commit()
            flash("Your Post Has Been Deleted!", "success")
        return redirect(url_for('main.home'))
    except:
        flash("Whoops! there's a problem deleting this post!", "success")
    return redirect(url_for('main.home'))
