# Face_Recog
The .py file uploaded here has been run on jupyter notebook.
A folder containing known faces to be trained is also uploaded.
A test video of the face_recognition is also uploaded.

Since this is a prototype and our team had to somehow complete before deadline, we have used a rather unsophisticated method of face recognition.
We still were not able to use the .h5 file and so couldn't go along the approach suggested by our mentors i.e. to use the YOLO and Siamese Network from keras/tensorflow.
We have currently implemented face recognition using a library named 'face_recognition' and 'OpenCV'

The basic methodology is still quite the same:
  1)Get a database of known images and train the model using functions in 'face_recognition'.
  2)Take input of a live video feed(requires webcam).
  3)Implement 'cnn' model to extract features from bounding box.
  4)Compare the features extracted using functions in 'face_recognition' with a certain tolerance level for %match.
  5)Display the matched name if tolerance is passed.
  
We will definitely try our very best to implement our mentor's approach after the mid-evaluation.
  
In the video(Test_video) of the working face recognition, due to lack of actual webcam there is delay in transmission as I use my phone as a replacement for the webcam. 

Due to personal reasons(Travelling) RamaKrishna wasn't actively participating.
Thank You.
