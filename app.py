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
from flask import render_template, send_from_directory,request, redirect
app = Flask(__name__)

app.config["OCpR_file_UPLOADS"] = ".\\uploads"
app.config["ALLOWED_OCpR_file_EXTENSIONS"] = ["XLSX", "XLS"]


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
        # print("File to Elaborate:")
        # print(request.query_string.replace('fileName=', ''))
        print(request.args.get('fileName'))
        data = CChe.comb_estimator('.\\uploads\\' + request.args.get('fileName'))
        

    #return render_template("index.html")
    return data
   
@app.route("/advantages", methods=["GET"])
def advantages():
    
    return jsonify(CC.AdvantageDisadvantageCal())


@app.route("/competitveness", methods=["GET"])
def competitveness():

    print("Working?")
 
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


  

if __name__ == '__main__':
    app.run()
