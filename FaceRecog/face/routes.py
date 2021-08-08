import os
import cv2
import numpy as np
import face_recognition
from werkzeug.utils import secure_filename
from face import app
from flask import render_template, url_for, flash, redirect, request, Response
from face.models import User
from face.forms import RegisterForm, LoginForm
from face import db
from flask_login import login_user, logout_user

params = {"local_server": "True",
          "upload_location":"Faces"
         }

ALLOWED_EXTENSIONS = {'jpg'}

KNOWN_FACES_DIR = "Faces"

app.config['UPLOAD_FOLDER'] = params['upload_location']
@app.route('/')
@app.route('/home')
def home_page():
    return render_template('home.html')



@app.route('/register', methods=['GET', 'POST'])
def register_page():
    form = RegisterForm()
    if form.validate_on_submit():
        user_to_create = User(username=form.username.data,
                              email_address=form.email_address.data,
                              password= form.password1.data)
        db.session.add(user_to_create)
        db.session.commit()
        return redirect(url_for('home_page'))
    if form.errors != {}:
        for err_msg in form.errors.values():
            flash(f'There was an error in creating a user: {err_msg}', category='danger')

    return render_template('register.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login_page():
    form = LoginForm()
    if form.validate_on_submit():
        attempted_user = User.query.filter_by(username=form.username.data).first()
        if attempted_user and attempted_user.check_password_correction(
                attempted_password=form.password.data
        ):
            login_user(attempted_user)
            flash(f'You are now logged in as: {attempted_user.username} ', category='success')
            return redirect(url_for('home_page'))
        else:
            flash('Username and Password dont match! Please Try Again', category='danger')
    return render_template('login.html', form = form)

@app.route('/logout')
def logout_page():
    logout_user()
    flash('You have been logged out ', category='info')
    return redirect(url_for("home_page"))



def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

path = 'Faces'
image_names = []
known_images = []
listknown=[]
mylist = os.listdir(path)


@app.route('/upload', methods=['GET', 'POST'])
def upload_file():

    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        name = request.form.get('name')
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            flash('No selected file', category='danger')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(name+'.jpg')
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            flash('Image successfully uploaded! ', category='Success')

            path1 = "Faces/" + filename + ".jpg"
            curImg1 = cv2.imread(path1)
            known_images.append(curImg1)
            image_names.append(filename)
            encode1 = face_recognition.face_encodings(curImg1)[0]
            listknown.append(encode1)
            return redirect(url_for('home_page',filename=filename))

        return render_template('upload.html')

for cl in mylist:
    curImg = cv2.imread(f'{path}/{cl}')
    known_images.append(curImg)
    image_names.append(os.path.splitext(cl)[0])

for img in known_images:
    encode = face_recognition.face_encodings(img)[0]
    listknown.append(encode)

def Video():
    global video
    video = cv2.VideoCapture(cv2.CAP_V4L2)

    while True:
        success, frame = video.read()
        if not success:
            break
        else:
            current_frame = face_recognition.face_locations(frame)
            encode_frame = face_recognition.face_encodings(frame, current_frame)

            for encoded, face_location in zip(encode_frame, current_frame):
                m = face_recognition.compare_faces(listknown, encoded)
                distance = face_recognition.face_distance(listknown, encoded)

                i = np.argmin(distance)
                x = np.min(distance)
                if m[i]:
                    if x < 0.5:
                        name = image_names[i].upper()
                    else:
                        name = "Unknown"

                    y1, x2, y2, x1 = face_location
                    cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                    cv2.rectangle(frame, (x1, y2 - 35), (x2, y2), (0, 255, 0), cv2.FILLED)
                    cv2.putText(frame, name, (x1 + 6, y2 - 6), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)

        ret, buffer = cv2.imencode('.jpg', frame)
        frame = buffer.tobytes()
        yield(b'--frame\r\n' 
              b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')




@app.route('/recognize',methods = ['POST', 'GET'])
def recognize_page():
    return render_template('face.html')

@app.route('/recognize/live', methods = ['POST','GET'])
def video_feed():
    global video
    video = cv2.VideoCapture(cv2.CAP_V4L2)
    return Response(Video(),mimetype='multipart/x-mixed-replace; boundary=frame')


