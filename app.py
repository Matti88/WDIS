#set FLASK_ENV=development

import os
import mimetypes 
import copy
import pandas as pd
import Conf_Calculator as CC
import Conf_Checker as CE
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
                data = CE.comb_estimator(file_target_save)
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
        data = CE.comb_estimator('.\\uploads\\' + request.args.get('fileName'))
        

    #return render_template("index.html")
    return data
   


@app.route("/launchProcess_OCpR_file", methods=["GET"])
def launchProcess():
    '''
    Route Process Function: start to process the OCpR
    '''
    
    if request.method == "GET":
        # print("File to Elaborate:")
        # print(request.query_string.replace('fileName=', ''))
        # print(request.args.get('fileName'))
        name_of_the_file = request.args.get('fileName')
        file_ = os.getcwd() + r"\uploads" + '\\' + name_of_the_file 


        dfs, details_dfs                    = CC.dataframes_splitter(path_to_the_file=file_)
        OCpR                                = CC.loop_thru_dataframes(dfs)
        OCpR_staked, OCpR_tags              = CC.OCpR_stacker(OCpR)
        details_dfs.insert(0,OCpR_staked)
        df_ca                               = CC.loop_thru_dataframes(details_dfs, howhow='left')

        #ListPrices
        df_ca['q_by_Lp'] = df_ca['List_Price'] * df_ca['qty']
        df_ca = df_ca.fillna(0.0)
        Conf_List_prices = df_ca[['code','q_by_Lp']].groupby('code').sum()
        Conf_List_prices['code'] = Conf_List_prices.index
        Conf_List_prices.index = Conf_List_prices.index.rename('index')

        #StreetPrices
        df_ca['q_by_Sp'] = df_ca['Street_Price'] * df_ca['qty']
        df_ca = df_ca.fillna(0.0)
        Conf_Street_prices = df_ca[['code','q_by_Sp']].groupby('code').sum()
        Conf_Street_prices['code'] = Conf_List_prices.index
        Conf_Street_prices.index = Conf_Street_prices.index.rename('index')

        final_df = pd.merge(OCpR_tags,Conf_List_prices, on='code', how='inner')
        final_df = pd.merge(final_df,Conf_Street_prices, on='code', how='inner')

        lod = []
        points = list(zip(final_df['q_by_Lp'].to_list(), final_df['q_by_Sp'].to_list()))
        for elem in points:
            lod.append({'x':elem[0], 'y':elem[1]})

        resultForChartJS = {'datasets': [{
            'label': 'Scatter Competition Points',
            'data': lod
            }]
        }

    return jsonify(resultForChartJS)


  

if __name__ == '__main__':
    app.run()
