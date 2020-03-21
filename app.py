#set FLASK_ENV=development

import os
from flask import Flask
from flask import render_template, send_from_directory,request, redirect
app = Flask(__name__)

app.config["OCpR_file_UPLOADS"] = "C:\\Users\\zuzan\\Desktop\\Projects\\steal\\uploads"
app.config["ALLOWED_OCpR_file_EXTENSIONS"] = ["XLX"]

def allowed_image(filename):
    '''
    Utility Function: Decides if a document should pass or not
    '''
    if not "." in filename:
        return False

    ext = filename.rsplit(".", 1)[1]

    if ext.upper() in app.config["ALLOWED_OCpR_file_EXTENSIONS"]:
        return True
    else:
        return False

@app.route('/')
@app.route('/index')
def hello():
    ''''
    Route Function: main page
    '''
    return render_template("index.html")


@app.route('/static/<path:path>')
def send_js(path):
    '''
    Route Utility: serves the static files. If they are updated then no re-uploas
    '''
    return send_from_directory('static', path)

@app.route("/upload-OCpR_file", methods=["GET", "POST"])
def upload_OCpR_file():
    '''
    Route Process Function: uploads the OCpR file
    '''

    if request.method == "POST":

        if request.files:

            OCpR_file = request.files["OCpR_file"]

            if OCpR_file.filename == "":
                print("No filename")
                return redirect("index")

            if allowed_image(OCpR_file.filename):
                OCpR_file.save(os.path.join(app.config["OCpR_file_UPLOADS"], OCpR_file.filename))

                print("OCpR_file saved")

    return redirect("index")

    

if __name__ == '__main__':
    app.run()
