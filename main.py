import cherrypy
import json
import parking
import cherrypy
import cv2

class Server(object):
    @cherrypy.expose
    def index(self):
        if cherrypy.request.headers['content-type'] == 'x-www-form-urlencoded' and cherrypy.request.method == 'POST':
            #length = int(cherrypy.request.headers['content-length'])
            #json_string = cherrypy.request.body.read(length).decode("utf-8")
            #data = json.loads(json_string)
            if cherrypy.request.headers['command'] == 'analyze':
                site = cherrypy.request.headers['site'];
                isDay = bool(cherrypy.request.headers['isDay']);
                busy, free = parking.parkingDataProcessing(site, isDay);
                img_file = open("frame.jpg").read()
                return json.dumps({'image': img_file.encode('base64'),'busy': busy, 'free':free})
        else:
            return open(os.path.join(MEDIA_DIR, u'index.html'))

cherrypy.quickstart(Server())
