from flask.app import Flask
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField, FileField
from wtforms.validators import DataRequired, Length, EqualTo, ValidationError


class RegistrationForm(FlaskForm): 
    username = StringField('Username', 
                            validators=[DataRequired(), Length(min=3, max=20)])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('ConfirmPassword', 
                            validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign up')


class LoginForm(FlaskForm):
    username = StringField('Username', 
                            validators=[DataRequired(), Length(min=3, max=20)])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')


class PostForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    content = TextAreaField('Description', validators=[DataRequired()])
    file = FileField('Image', validators=[DataRequired()])
    submit = SubmitField('Post')

class CommentForm(FlaskForm):
    content = StringField('Description', validators=[DataRequired()])
    submit = SubmitField('Comment')

class DeleteForm(FlaskForm):
    post_id = StringField('ID')
    comment_id = StringField('ID')
    del_type = StringField('ID')
    submit = SubmitField('Hide/Show')

class AdminForm(FlaskForm):
    post_id = StringField('ID')
    comment_id = StringField('ID')
    del_type = StringField('ID')
    submit = SubmitField('Delete')

class SearchForm(FlaskForm):
    query = StringField('Search', validators=[Length(min=3, max=20)])
    submit = SubmitField('Search')