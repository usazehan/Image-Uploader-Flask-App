import os

from werkzeug import secure_filename
from flask import Flask, request, render_template, send_from_directory, redirect

app = Flask(__name__)

APP_ROOT = os.path.dirname(os.path.abspath(__file__))

extension = set(['png', 'jpg', 'jpeg', 'gif', 'tif'])
# Only function only allows image file types
def allowed_file(filename):
    return '.' in filename and  \
        filename.rsplit('.', 1)[1].lower() in extension

@app.route("/")
def index():
    return render_template("upload.html")

@app.route("/upload", methods=["POST"])
def upload():
    target = os.path.join(APP_ROOT, 'images/')
    print(target)
    # creates a folder called "images" if not done so
    if not os.path.isdir(target):
            os.mkdir(target)
            print("Created a upload directory")
    else:
        print("Couldn't create upload directory: {}".format(target))
    print(request.files.getlist("file"))
    if 'file' not in request.files:
        raise Exception("No file part")
        return redirect('/')
    file = request.files['file']
    if file.filename == '':
        raise Exception("No selected file")
        return redirect('/')
    if file and allowed_file(file.filename):
        for upload in request.files.getlist("file"):
            print(upload)
            print("{} is the file name".format(upload.filename))
            filename = secure_filename(upload.filename)
            
            destination = "/".join([target, filename])
            print ("Accept incoming file:", filename)
            print ("Save it to:", destination)
            upload.save(destination)

    return render_template("display_image.html", image_name=filename)

@app.route('/upload/<filename>')
def send_image(filename):
    return send_from_directory("images", filename)

if __name__ == "__main__":
    app.run(port=4555, debug=True)
