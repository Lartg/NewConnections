from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os
from flask_migrate import Migrate
import psycopg2
import dotenv
dotenv.load_dotenv('.env')


app = Flask(__name__)
app.secret_key = os.urandom(24)


migrate = Migrate(compare_type=True)

db = SQLAlchemy()

uri = os.environ.get('DATABASE_URL').replace('postgres', 'postgresql')
app.config['SQLALCHEMY_DATABASE_URI'] = uri
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)


conn = psycopg2.connect(
  dbname=os.environ.get('DB_NAME'),
  user=os.environ.get('DB_USER'),
  password=os.environ.get('DB_PASSWORD'),
  host=os.environ.get('DB_HOST'),
  port=5432
  )

  #sslmode='require'

db.app = app

migrate.init_app(db, app)
from FlaskApp.routes import main
import FlaskApp.google_auth as google_auth
app.register_blueprint(google_auth.auth)
app.register_blueprint(main)