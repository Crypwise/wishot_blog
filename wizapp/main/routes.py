from flask import Blueprint, request, render_template, flash
from flask_login import login_required, current_user
from flask_mail import Message

from wizapp import mail
from wizapp.models import Post, User

main = Blueprint('main', __name__)


@main.route("/")
def home():
    page = request.args.get('page', 1, type=int)
    posts = Post.query.order_by(Post.date_posted.desc()).paginate(page=page, per_page=4)
    return render_template("index.html", posts=posts)


@main.route('/blog')
def blog():
    page = request.args.get('page', 1, type=int)
    posts = Post.query.order_by(Post.date_posted.desc()).paginate(page=page, per_page=8)
    return render_template("blog.html", posts=posts)


@main.route("/about")
def about():
    return render_template("about.html")


@main.route("/gossips")
def gossips():
    page = request.args.get('page', 1, type=int)
    posts = Post.query.filter_by(categories="GOSSIPS").order_by(Post.date_posted.desc()).paginate(page=page, per_page=8)
    return render_template("gossips.html", posts=posts)


@main.route("/top_news")
def top_news():
    page = request.args.get('page', 1, type=int)
    posts = Post.query.filter_by(categories="TOP NEWS").order_by(Post.date_posted.desc()).paginate(page=page,
                                                                                                   per_page=8)
    return render_template("top_news.html", posts=posts)


@main.route("/crypto")
def crypto():
    page = request.args.get('page', 1, type=int)
    posts = Post.query.filter_by(categories="CRYPTO").order_by(Post.date_posted.desc()).paginate(page=page, per_page=8)

    return render_template("crypto.html", posts=posts)


@main.route("/sports")
def sports():
    page = request.args.get('page', 1, type=int)
    posts = Post.query.filter_by(categories="SPORTS").order_by(Post.date_posted.desc()).paginate(page=page, per_page=8)
    return render_template("sports.html", posts=posts)


@main.route("/lifestyle")
def lifestyle():
    page = request.args.get('page', 1, type=int)
    posts = Post.query.filter_by(categories="LIFESTYLE").order_by(Post.date_posted.desc()).paginate(page=page,
                                                                                                    per_page=8)
    return render_template("lifestyle.html", posts=posts)


@main.route("/entertainment")
def entertainment():
    page = request.args.get('page', 1, type=int)
    posts = Post.query.filter_by(categories="ENTERTAINMENT").order_by(Post.date_posted.desc()).paginate(page=page,
                                                                                                        per_page=8)
    return render_template("entertainment.html", posts=posts)


@main.route("/relationship")
def relationship():
    page = request.args.get('page', 1, type=int)
    posts = Post.query.filter_by(categories="RELATIONSHIP").order_by(Post.date_posted.desc()).paginate(page=page,
                                                                                                       per_page=8)
    return render_template("relationship.html", posts=posts)


@main.route('/contact', methods=['GET', 'POST'])
def contact():
    user = User
    if request.method == 'POST':
        name = request.form.get('name')
        subject = request.form.get('subject')
        email = request.form.get('email')
        message = request.form.get('message')
        msg = Message(f'New Message from {email}', sender=f'{user.email}',
                      recipients=['wishotstudio@gmail.com'])
        msg.body = f"""
 Name :  {name}

Email :  {email}

Subject :  {subject}

Message :  {message}

           """
        mail.send(msg)
        flash('your message have been sent', 'success')

    return render_template('contact.html', title='contact Form')
