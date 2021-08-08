import cv2
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///face.db'
app.config['SECRET_KEY']= 'd08fc2fa3bcfd97bb184bf38'
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
params = {"local_server": "True",
          "admin_user": "face_recognition",
          "admin_password": "abp",
          "upload_location":"ImageBasics"
         }

app.config['UPLOAD_FOLDER']=params['upload_location']
app.secret_key = 'super-secret-key'

cam = cv2.VideoCapture(0)
from face import routes
