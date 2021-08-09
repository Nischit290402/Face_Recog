# Face_Recog

The Backend program :

The code is in the .py file and has been run on jupyter notebook as shown in Test_Video.

A folder containing known faces to be trained is also uploaded.

A test video of the face_recognition is also uploaded.

We have currently implemented face recognition using a library named 'face_recognition' and 'OpenCV'

The basic methodology is still quite the same as compared to the standard FaceNet and YOLO application put together:

  1)Get a database of known images and train the model using functions in 'face_recognition'.

  2)Take input of a live video feed(requires webcam).
  
  3)Implement 'cnn' model to extract features from bounding box.
  
  4)Compare the features extracted using functions in 'face_recognition' with a certain tolerance level for %match.
  
  5)Display the matched name if tolerance is passed.
  
The Frontend program:
  
    The frontend program is purely an implementation of FLASK using python and html. 
  
    To support the styles we have used BOOTSTRAP, CSS
  
    The structuring of the frontend into html and python files has been accomplished using a library of FLASK called JENGO.
  
  While debugging for user-friendly purposes, another library called WERKZEUG
  
  A database called face.db is made in order to store user info. However, the images uploaded is not stored here for the purpose of easy access by the OpenCV.
  
  A different folder called Faces replaces the known_faces during deployment of code.
  
  
  
  
  
  #Thank You
