import cherrypy
import json
import parking
import cherrypy
import cv2
import os
from flask import Flask
from flask import request
from flask import render_template
import base64

URL_PATH = '84.201.147.156'
LISTEN = '0.0.0.0'
PATH = os.path.abspath("../")

app = Flask(__name__,static_folder='static')

@app.route("/",methods=['POST', 'GET'])
def hello():
    print(request.form)
    name = "none"
    if request.content_type:
        print(request.content_type, request.method, request.form['command'])
        if request.content_type == 'application/x-www-form-urlencoded; charset=UTF-8' and request.method == 'POST':
            print("2")
            if 'command' in request.form and request.form['command'] == 'analyze':
                print("3")
                site = request.form['site'];
                isDay = bool(request.form['isDay']);
                free, buse = parking.parkingDataProcessing();

                return json.dumps({'busy': buse, 'free':free})
        else:
            print("4")
            return render_template('index.html',name=name)
    else:
        print("5")
        return render_template('index.html',name=name)

@app.route("/getimage")
def getImage():
    return open("frame.jpg")


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080)
