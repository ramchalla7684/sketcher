from flask import render_template, request, send_from_directory, send_file
import base64
import json
import uuid
import os
from sketch_recognizer import recognize

def init(app):
    @app.route("/")
    def homepage():
        return render_template('index.html')

    @app.route("/images/<filename>")
    def send_image(filename):
        return send_from_directory('../images/archive/', filename)

    @app.route("/api/upload", methods=['POST'])
    def upload():
        try:
            img = request.json['img']
            img = base64.b64decode(img)
            sketch_file_path = '../images/sketches/' + str(uuid.uuid4()).replace('-', '_') + '.png'
            sketch_file = open(sketch_file_path, "wb")
            sketch_file.write(img)
            sketch_file.close()
            images = recognize(sketch_file_path)
            images = list(map(lambda image: ('/images/'+image), images))
            return json.dumps(images)
        except:
            print("Something went wrong")
            response = {'success': False, 'message': "Something went wrong"}
            return json.dumps(response)