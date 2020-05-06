

import flask
import os
import cv2
from flask import Flask , render_template , request , send_file


app = Flask(__name__)

name = ''

classifier = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

ALLOWED_EXT = set(['jpg' , 'jpeg' , 'png'])
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXT

@app.route("/")
def home():
	return render_template("index.html")

@app.route('/success' , methods = ['POST'])
def success():
	error = None
	#using request module to check if request method is POST or not
	if request.method == 'POST':
		#storing the image 
		file = request.files['file']
		#storing the path of images folder in target
		target = os.path.join(os.getcwd() , 'images')
		if file and allowed_file(file.filename):
			#saving the input images in images/img folder
			file.save(os.path.join(target , 'img' , file.filename))
			#reading the input image
			img = cv2.imread(os.path.join(target , 'img' , file.filename))
			#converting the image to grayscale
			gray = cv2.cvtColor(img , cv2.COLOR_BGR2GRAY)
			#detecting the face through classifier and using cv2.blur to blur it
			faces = classifier.detectMultiScale(gray , 1.1 , 4)
			for (x, y, w, h) in faces:
				img[y:y+h , x:x+w] = cv2.blur(img[y:y+h , x:x+w], (90, 90) , 50)
			
			#saving the papth of blur_img folder in new_target
			new_target = os.path.join(target , 'blur_img')
			name = file.filename
			#saving the blur image in blur_img folder(new_target)
			cv2.imwrite(os.path.join(new_target , file.filename), img)
			#rendering the success.html page in response and saving the image name to name
			return render_template("success.html" , name = file.filename)
		else:
			error = "PLease upload a photo!"
			#error message to be displayed if image extension is different
			#id user clicks the upload button withoutuploading an image
			return render_template("index.html" , error = error)

@app.route('/get_image/<filename>')
def get_image(filename):
	target = os.path.join(os.getcwd() , 'images')
	new_target = os.path.join(target , 'blur_img')
	name = os.path.join(new_target , filename)
	return send_file(name)

@app.route('/use')
def use():
	return render_template("use.html")



if __name__ == "__main__":
	app.run(debug = True)