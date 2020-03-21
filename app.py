

#set FLASK_ENV=development


from flask import Flask
from flask import render_template, send_from_directory
app = Flask(__name__)


@app.route('/')
@app.route('/index')
def hello():
    return render_template("index.html")


@app.route('/static/<path:path>')
def send_js(path):
    return send_from_directory('static', path)

if __name__ == '__main__':
    app.run()
