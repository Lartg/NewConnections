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
  image = StringField('Image')
  submit = SubmitField('Submit')


class EditAccountForm(FlaskForm):
  username = StringField('Username',
    validators=[
      DataRequired(),
      Length(min=4, max=20, message=None)])
  name = StringField('Name',
    validators=[
      DataRequired()
    ])
  image = StringField('Image')
  profile_bio = StringField('Bio')
  submit = SubmitField('Submit')


class CommentForm(FlaskForm):
  content = StringField('Comment')
  post = IntegerField('Post')
  submit = SubmitField('Submit')