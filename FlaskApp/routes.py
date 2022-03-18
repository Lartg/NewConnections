from flask import Blueprint, render_template, request, flash, redirect, session, make_response
from FlaskApp.forms import CommentForm,  PostForm, EditAccountForm
from FlaskApp.models import Post, User, Comment, Like
from FlaskApp import db, app
from authlib.client import OAuth2Session
import google.oauth2.credentials
import googleapiclient.discovery
import json

import FlaskApp.google_auth as google_auth
main = Blueprint('main', __name__)

# with app.app_context():
#    db.create_all()


#------------------content------------------------------------------------------------

@main.route('/')
def landing_page():
  if google_auth.is_logged_in() == True:
    user_info = google_auth.get_user_info()
    user = User.query.filter_by(email=user_info['email']).first()
    if user:
      return redirect(f'/feed/{user.id}')
    else:
      new_user = User(
        username=user_info['given_name'],
        email=user_info['email'],
        name=user_info['given_name'],
      )
      db.session.add(new_user)
      db.session.commit()
      return redirect(f'/account-profile/{new_user.id}/edit')

  return render_template('landing_page.html', user=None)

@main.route('/feed/<user_id>', methods = ['GET', 'POST'])
def display_feed(user_id):
  if google_auth.is_logged_in():
    user = User.query.get(user_id)
    posts = Post.query.all()
    comments = Comment.query.all()
    form = CommentForm()
    if form.is_submitted():
      new_comment = Comment(
        content = form.content.data,
        author = user.username,
        owner = user_id,
        post_id = form.post.data
      )
      db.session.add(new_comment)
      db.session.commit()
      return render_template('feed.html', posts=posts, user=user, form=form, comments=Comment.query.all())
    return render_template('feed.html', posts=posts, user=user, form=form, comments = comments)
  return flash('You are not currently logged in.')

@main.route('/create-post/<user_id>', methods = ['GET', 'POST'])
def create_post(user_id):
  if google_auth.is_logged_in():
    user = User.query.get(user_id)
    form = PostForm()
    if form.is_submitted():
      author = user.username
      # image = request.form['photo-url']
      # print(image)
      new_post = Post(
        time_created = form.time.data,
        title = form.title.data,
        description = form.description.data,
        owner = user_id,
        author = author
        #image = image
      )
      db.session.add(new_post)
      db.session.commit()
      return redirect(f'/feed/{user_id}')
    
    return render_template('create_post.html', form=form, user=user)
  return flash('You are not currently logged in.')

@main.route('/account-profile/<user_id>')
def account_profile(user_id):
  if google_auth.is_logged_in():
    user_info = google_auth.get_user_info()
    user = User.query.filter_by(email=user_info['email']).first()
    user_profile = User.query.get(user_id)
    posts = Post.query.filter_by(owner=user_id)
    return render_template('account_profile.html', user=user, posts=posts, profile=user_profile)
  return flash('You are not currently logged in.')

@main.route('/account-profile/<user_id>/edit', methods = ['GET', 'POST'])
def edit_profile(user_id):
  if google_auth.is_logged_in():
    user = User.query.get(user_id)
    form = EditAccountForm(obj=user)
    if form.is_submitted():
      print('-------------------------1------------')
      user.username = form.username.data
      user.name = form.name.data
      user.profile_picture = form.image.data
      print(form.image.data)
      print('-------------------------1------------')
      user.profile_bio = form.profile_bio.data
      db.session.add(user)
      db.session.commit()
      return redirect(f'/account-profile/{user_id}')
    return render_template('edit_profile.html', user=user, form=form)
  return flash('You are not currently logged in.')



# #------DELETE----------------------------------------------------------------------

@main.route('/delete-user/<user_id>')

def delete_user(user_id):
  if google_auth.is_logged_in():
    user = User.query.get(user_id)
    #delete all posts
    db.session.delete(user)
    db.session.commit()
    return redirect('/google/logout')
  return flash('You are not currently logged in.')

@main.route('/delete-post/<post_id>')
def delete_post(post_id):
  if google_auth.is_logged_in():
    user_info = google_auth.get_user_info()
    user = User.query.filter_by(email=user_info['email']).first()
    post = Post.query.get(post_id)
    db.session.delete(post)
    db.session.commit()
    return redirect(f'/feed/{user.id}')
  return flash('You are not currently logged in.')

@main.route('/delete-comment/<comment_id>')
def delete_comment(comment_id):
  if google_auth.is_logged_in():
    user_info = google_auth.get_user_info()
    user = User.query.filter_by(email=user_info['email']).first()
    comment = Comment.query.get(comment_id)
    db.session.delete(comment)
    db.session.commit()
    return redirect(f'/feed/{user.id}')
  return flash('You are not currently logged in.')

