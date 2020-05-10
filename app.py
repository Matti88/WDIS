#set FLASK_ENV=development

import os
import mimetypes 
import copy
import pandas as pd
import Conf_Calculator as CC
import Conf_Checker as CChe
import json
from flask import jsonify
from flask import Flask
from flask import render_template, send_from_directory,request, redirect, make_response, request


from flask import Flask, jsonify, request
from flask_jwt_extended import (
    JWTManager, jwt_required, create_access_token,
    get_jwt_identity
)


app = Flask(__name__)

# Setup the Flask-JWT-Extended extension
app.config['JWT_SECRET_KEY'] = 'super-secret'  # Change this!
jwt = JWTManager(app)


app.config["OCpR_file_UPLOADS"] = ".\\uploads"
app.config["ALLOWED_OCpR_file_EXTENSIONS"] = ["XLSX", "XLS"]


# Provide a method to create access tokens. The create_access_token()
# function is used to actually generate the token, and you can return
# it to the caller however you choose.
@app.route('/login', methods=['POST'])
def login():
    if not request.is_json:
        return jsonify({"msg": "Missing JSON in request"}), 400
    
    username = request.json.get('login', None)
    password = request.json.get('password', None)
 
    if not username:
        return jsonify({"msg": "Missing username parameter"}), 400
    if not password:
        return jsonify({"msg": "Missing password parameter"}), 400

    if username != 'test' or password != 'test':
        return jsonify({"msg": "Bad username or password"}), 401

    # Identity can be any data that is json serializable
    access_token = create_access_token(identity=username)
    return jsonify(access_token=access_token), 200


# Protect a view with jwt_required, which requires a valid access token
# in the request to access.
@app.route('/protected', methods=['GET'])
@jwt_required
def protected():
    # Access the identity of the current user with get_jwt_identity
    current_user = get_jwt_identity()
    return jsonify(logged_in_as=current_user), 200

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

 
@app.route('/access_page')  
def login_access():
    ''''
    Route Function: main page
    '''
    return render_template("login.html")


@app.route('/checker')
def cheker():
    ''''
    Route Function: main page
    '''
    return render_template("checker.html")




@app.route("/upload-OCpR_file", methods=["GET", "POST"])
def upload_OCpR_file():
    '''
    Route Process Function: uploads the OCpR file
    '''
    if request.method == "POST":
        print(request)
        if request.files:

            OCpR_file = request.files["file"]
            print(OCpR_file.filename)
            if allowed_image(OCpR_file.filename):
                file_target_save = os.path.join(app.config["OCpR_file_UPLOADS"], OCpR_file.filename)
                OCpR_file.save(file_target_save)
                print(file_target_save)
                data = CChe.comb_estimator(file_target_save)
            return data

    return ('', 204)
            
@app.route("/Checker_OCpR_file", methods=["GET"])
def Checker_OCpR():
    '''
    Route Process Function: start to process the OCpR
    '''
    data = None
    if request.method == "GET":
        data = CChe.comb_estimator('.\\uploads\\' + request.args.get('fileName'))
        

    #return render_template("index.html")
    return data


@app.route("/advantages", methods=["GET"])
@jwt_required
def advantages():
    print(request.form)
    return jsonify(CC.AdvantageDisadvantageCal())

@app.route("/confronts", methods=["GET"])
def Product_on_confrontation():
    return jsonify(CC.Product_on_confrontation())

@app.route("/competitveness", methods=["GET"])
def competitveness():

    return jsonify(CC.ThreatsOpportunitiesCal())


@app.route("/ListStreet", methods=["GET"])
def ListStreet():
    '''
    Route Process Function: start to process the OCpR
    '''
    if request.method == "GET":
        name_of_the_file = request.args.get('fileName')
        file_ = os.getcwd() + r"\uploads" + '\\' + name_of_the_file 
        resultForChartJS = CC.ListStreetCal(file_, D3_ChartJS = False)
 
    return jsonify(resultForChartJS)

@app.route("/sales_analysis", methods=["GET"])
def sales_analysis():
    '''
    Route Process Function: sales analysis 
    '''
    return jsonify( CC.sales_analysis_gen_matcher() )


if __name__ == '__main__':
    app.run()
