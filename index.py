from flask import Flask, request, render_template
from core import object_detect
import os

app = Flask(__name__)
app.config['TEMPLATES_AUTO_RELOAD'] = True
app.config["UPLOADS_PATH"] = './static/uploads'
app.config["OUTPUT_PATH"] = './static/uploads/output'

@app.route('/', methods=['POST', 'GET'])

def index():
    if request.method == 'POST' and 'image' in request.files:
        image = request.files["image"]

        path = os.path.join(app.config["UPLOADS_PATH"], image.filename)
        image.save(path)
        image_output = object_detect(path)

        return render_template('index.html', file=image.filename, output=image_output)
    else:
        return render_template('index.html', file=False)

# @app.after_request
# def add_header(r):
#     """
#     Add headers to both force latest IE rendering engine or Chrome Frame,
#     and also to cache the rendered page for 10 minutes.
#     """
#     r.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
#     r.headers["Pragma"] = "no-cache"
#     r.headers["Expires"] = "0"
#     r.headers['Cache-Control'] = 'public, max-age=0'
#     return r

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)