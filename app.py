import os
from flask import Flask, flash, request, redirect, url_for, render_template, send_from_directory
from werkzeug.utils import secure_filename
import numpy as np
import cv2
import sys
from twilio.rest import Client

UPLOAD_FOLDER = '/home/ubuntu/workspace/flaskserver/uploads'

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

face_cascade = cv2.CascadeClassifier('/usr/local/lib/python3.6/dist-packages/cv2/data/haarcascade_frontalface_default.xml')
fullbody_cascade = cv2.CascadeClassifier('/usr/local/lib/python3.6/dist-packages/cv2/data/haarcascade_fullbody.xml')
upperbody_cascade = cv2.CascadeClassifier('/usr/local/lib/python3.6/dist-packages/cv2/data/haarcascade_upperbody.xml')
lowerbody_cascade = cv2.CascadeClassifier('/usr/local/lib/python3.6/dist-packages/cv2/data/haarcascade_lowerbody.xml')

client = Client("AC1a26dcf08aabcb2a4916b80a6ac309a1","0d59c3c80fb5751ff59509c6dd32fdd0")

@app.route('/')
def image_stream():
    filename = 'stream.jpeg'
    return render_template("index.html", filename=filename)

@app.route('/uploads/<filename>')
def send_file(filename):
    return send_from_directory(UPLOAD_FOLDER, filename)

@app.route('/updebug', methods=['POST'])
def up_debug():
    if request.method=='POST':
        coord_output = 'no faces detected'
        upload_image_name = 'upload.jpeg'
        uploadname = os.path.join(app.config['UPLOAD_FOLDER'], upload_image_name)
        with open(uploadname,'wb') as file:
            file.write(request.data)
        
        
        img = cv2.imread(uploadname)
        stream_image_name = 'stream.jpeg'
        streamname = os.path.join(app.config['UPLOAD_FOLDER'], stream_image_name)
        
        if img is None:
            cv2.imwrite(streamname,img)
            return "Image Upload Failed: imread() returns None"
        else:
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            faces = face_cascade.detectMultiScale(gray, 1.3, 5)
            if len(faces) > 0:
                for (x,y,w,h) in faces:
                    coord_output = 'image detected: ' +str(x+w/2) + ' ' + str(y+h/2)
                    cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2)
                    cv2.imwrite(streamname,img)
                    client.messages.create(to="+17737505765", 
                       from_="+18722393239", 
                       body="Intruder Detected!")
                    break
            else:
                fullbodies = fullbody_cascade.detectMultiScale(gray, 1.3, 5)
                if len(fullbodies) > 0:
                    for (x,y,w,h) in fullbodies:
                        coord_output = str(x) + ' ' + str(y) + ' ' + str(w) + ' ' + str(h) + ' '
                        cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2)
                        cv2.imwrite(streamname,img)
                        break
                else:
                    upperbodies = upperbody_cascade.detectMultiScale(gray, 1.3, 5)
                    if len(upperbodies) > 0:
                        for (x,y,w,h) in upperbodies:
                            coord_output = str(x) + ' ' + str(y) + ' ' + str(w) + ' ' + str(h) + ' '
                            cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2)
                            cv2.imwrite(streamname,img)
                            break
                    else:
                        lowerbodies = lowerbody_cascade.detectMultiScale(gray, 1.3, 5)
                        if len(lowerbodies) > 0:
                            for (x,y,w,h) in lowerbodies:
                                coord_output = str(x) + ' ' + str(y) + ' ' + str(w) + ' ' + str(h) + ' '
                                cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2)
                                cv2.imwrite(streamname,img)
                                break
                cv2.imwrite(streamname,img)
        
        return str(coord_output)

@app.route('/imgup', methods=['POST'])
def img_up():
    if request.method=='POST':
        print('post request received')
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        #if file and allowed_file(file.filename):
        else:
            coord_output = ''
            filename = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
            file.save(filename)
            img = cv2.imread(filename)
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            faces = face_cascade.detectMultiScale(gray, 1.3, 5)
            for (x,y,w,h) in faces:
                coord_output = str(x+w/2) + ' ' + str(y+h/2)
            return str(coord_output)

if __name__ == "__main__":
    app.run(threaded=True)
