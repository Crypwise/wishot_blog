from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed, FileField
from wtforms import SubmitField, SelectField, TextAreaField, StringField
from wtforms.validators import DataRequired


class postForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    content = TextAreaField('Content', validators=[DataRequired()])
    categories = SelectField('Categories',
                             choices=[('Select Categories', 'Select Categories'),
                                      ('TOP NEWS', 'TOP NEWS'), ('CRYPTO', 'CRYPTO'), ('SPORTS', 'SPORTS'),
                                      ('GOSSIPS', 'GOSSIPS'), ('LIFESTYLE', 'LIFESTYLE'),
                                      ('ENTERTAINMENT', 'ENTERTAINMENT'),
                                      ('RELATIONSHIP', 'RELATIONSHIP')])
    image_post = FileField('select Picture', validators=[FileAllowed(['jpg', 'png', 'jpeg', 'gif', 'mp4'])])
    submit = SubmitField('Post')