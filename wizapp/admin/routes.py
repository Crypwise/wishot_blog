from flask import Blueprint, flash, redirect, render_template, url_for, request
from flask_login import login_required, current_user

from wizapp import db
from wizapp.admin.forms import UpdateAccountForm
from wizapp.models import User, Post
from wizapp.users.utils import save_picture

admin = Blueprint('admin', __name__)


@admin.route('/admin')
@login_required
def admin1():
    if current_user.email != 'WishotStudio@gmail.com':
        flash("Sorry you have to be an admin to access this page", "info")
        return redirect(url_for('main.home'))
    post = Post.query.all()
    user = User.query.all()
    return render_template("Admin/index.html", post=post, user=user)


@admin.route("/account", methods=['GET', 'POST'])
@login_required
def account():
    if current_user.email != 'WishotStudio@gmail.com':
        flash("Sorry you have to be an admin to asses this page", "info")
        return redirect(url_for('main.home'))
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        return redirect(url_for('admin.account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    image_file = url_for('static', filename='profile_pics/' + current_user.image_file)
    return render_template('Admin/account.html', title='Account', image_file=image_file, form=form)


@admin.route('/admin|tables')
@login_required
def admin_tables():
    if current_user.email != 'WishotStudio@gmail.com':
        flash("Sorry you have to be an admin to asses this page", "info")
        return redirect(url_for('main.home'))
    post = Post.query.all()
    user = User.query.all()
    return render_template("Admin/tables.html", post=post, user=user)


@admin.route('/admin|chart')
@login_required
def admin_chart():
    if current_user.email != 'WishotStudio@gmail.com':
        flash("Sorry you have to be an admin to asses this page", "info")
        return redirect(url_for('main.home'))
    return render_template("Admin/charts.html")
