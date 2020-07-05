# -*- coding: utf-8 -*-
"""
Created on Sat Jul  4 16:26:16 2020

"""

# -*- coding: utf-8 -*-
"""
Created on Fri Jul  3 04:19:24 2020

@author: 
"""

from flask import Flask, render_template, request
import pandas as pd
import cv2
import numpy as np
import base64
#from flask.ext.cors import cross_origin
from flask_cors import CORS, cross_origin
from flask import jsonify

app = Flask(__name__)
#app.config['CORS_HEADERS'] = 'Content-Type'
CORS(app)
#cors = CORS(app, resources={r"/add_face": {"origins": "http://localhost:3000"}})


template = cv2.imread("tej_web2.jpg", cv2.IMREAD_GRAYSCALE)
w, h = template.shape[::-1]

cascPath = "haarcascade_frontalface_default.xml"
faceCascade = cv2.CascadeClassifier(cascPath)
first = True
clip_face = []

@app.route('/faceMonitering', methods=['GET', 'POST'])
#@cross_origin(origin='*',headers=['access-control-allow-origin','Content-Type'])
@cross_origin(origin='http://localhost:4200',headers=['Content-Type','Access-Control-Allow-Origin'])
#@cross_origin()
def faceMonitering():
    global first
    global clip_face
    if request.method == 'POST':
        #  read encoded image
        #print(request.json)
        imageString = base64.b64decode(request.json['img'])
        #print(imageString)

        #  convert binary data to numpy array
        nparr = np.fromstring(imageString, np.uint8)
        #print(nparr)

        #  let opencv decode image to correct format
        img = cv2.imdecode(nparr, cv2.IMREAD_ANYCOLOR);
        #img = cv2.imdecode(nparr, 1);
#        cv2.imshow("frame", img)
#        cv2.waitKey(0)
#        cv2.destroyAllWindows()
        gray_frame = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        faces = faceCascade.detectMultiScale(
            gray_frame,
            scaleFactor=1.1,
            minNeighbors=5,
            minSize=(30, 30),
        )
        
        if(np.size(faces) > 0):
            if(first == True):
                x,y,h,w = faces[0]
                clip_face = gray_frame[y:y+h, x:x+w]
                cv2.imwrite("detected-boxes.jpg", clip_face)
                first = False
        
        res = cv2.matchTemplate(gray_frame, clip_face, cv2.TM_CCOEFF_NORMED)
        loc = np.where(res >= 0.7)
        
        if(np.size(faces) == 0):
            print('Fail')
            retval =False
            errormsg = 'No Person Available'
        elif(faces.shape[0] == 1):
            print('Success')
            if(np.size(loc) > 0):
                retval = True
                errormsg = 'Success'
            else:
                retval =False
                errormsg = 'Not the same person'
        else:
            print('Fail')
            retval =False
            errormsg = 'More Than One Person Available'
        #cv2.imwrite('tej_web.jpg', img)
            
        
    return jsonify({"error": errormsg, "valid": retval})


if __name__ == '__main__':
    app.run(debug=True, use_reloader=False, port=5000)