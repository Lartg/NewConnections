from flask_wtf import FlaskForm
from flask import flash
from wtforms import StringField, DateField, SelectField, SubmitField, IntegerField
from wtforms_sqlalchemy import fields
from wtforms.validators import DataRequired, Length, ValidationError, NumberRange


class PostForm(FlaskForm):
  time = DateField('Time of Event')
  title = StringField('Post Title',
    validators=[
      DataRequired(),
      Length(min=3, max = 50, message='Your Title needs to be within 3 and 50 characters')
    ])
  description = StringField('Post Description',
    validators=[
      DataRequired()
    ])
  submit = SubmitField('Submit')


class LoginForm(FlaskForm):
  username = StringField('Username',
    validators=[
      DataRequired(),
      Length(min=4, max=20, message=None)])
  password = StringField('Password',
    validators=[
    DataRequired(),
    Length(min=4, max=20, message=None)])
  submit = SubmitField('Submit')
  
class SignUpForm(FlaskForm):
  username = StringField('Username')
  password = StringField('Password')
  submit = SubmitField('Submit')
  
  # def validate_username(self, username):
  #   user = User.query.filter_by(username=username.data).first()
  #   if user:
  #     raise ValidationError('That username is taken. Please choose a different one.')

class EditAccountForm(FlaskForm):
  username = StringField('Username',
    validators=[
      DataRequired(),
      Length(min=4, max=20, message=None)])
  name = StringField('Name',
    validators=[
      DataRequired()
    ])
  profile_bio = StringField('Bio')
  submit = SubmitField('Submit')
  #image = ImageField()
  # in imagefield class manual_crop='100x100'

class CommentForm(FlaskForm):
  content = StringField('Comment')
  post = IntegerField('Post')
  submit = SubmitField('Submit')