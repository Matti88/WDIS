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
   
@app.route("/advantages", methods=["GET"])
def advantages():
    Competitor0 = CC.AnalysisDF(r'C:/Users/zuzan/Desktop/MyCompany.xls')
    Competitor1 = CC.AnalysisDF(r'C:/Users/zuzan/Desktop/Competitor.xls')

    Comp0 = pd.concat([Competitor0[list(filter(lambda x: 'tag' in x,  Competitor0.columns))], Competitor0[['q_by_Lp','q_by_Sp']] ] , axis=1)
    Comp1 = pd.concat([Competitor1[list(filter(lambda x: 'tag' in x,  Competitor1.columns))], Competitor1[['q_by_Lp','q_by_Sp']] ] , axis=1)

    Comp0_grouped = Comp0.groupby(list(filter(lambda x: 'tag' in x,  Comp0.columns))).mean().reset_index() 
    Comp1_grouped = Comp1.groupby(list(filter(lambda x: 'tag' in x,  Comp1.columns))).mean().reset_index() 


    cmmn_tags_list = list(filter(lambda x: not(('q_by_Lp' in x) or ('q_by_Sp' in x)) , CC.common_tags(Comp0_grouped, Comp1_grouped)))

    ocpr_df = pd.merge(Comp0_grouped, Comp1_grouped, on=cmmn_tags_list ,how='inner', suffixes=('_0', '_1'))     

    MyCompany_LP_Advantage = ocpr_df[ocpr_df['q_by_Lp_0'] < ocpr_df['q_by_Lp_1']].to_json(orient="records")
    MyCompany_SP_Advantage = ocpr_df[ocpr_df['q_by_Sp_0'] < ocpr_df['q_by_Sp_1']].to_json(orient="records")
    Competitor_SP_Advantage = ocpr_df[ocpr_df['q_by_Sp_0'] > ocpr_df['q_by_Sp_1']].to_json(orient="records")
    Competitor_LP_Advantage = ocpr_df[ocpr_df['q_by_Lp_0'] > ocpr_df['q_by_Lp_1']].to_json(orient="records")

    competition_Vantages = "{" + f""" "MyCompany_LP_Advantage" : {MyCompany_LP_Advantage}
                                    , "MyCompany_SP_Advantage" : {MyCompany_SP_Advantage} 
                                    , "Competitor_SP_Advantage" : {Competitor_SP_Advantage} 
                                    , "Competitor_LP_Advantage" : {Competitor_LP_Advantage} """ + "}"

    file_like_object = json.loads(competition_Vantages)

    return jsonify(file_like_object)


@app.route("/competitveness", methods=["GET"])
def competitveness():
    Competitor0 = CC.AnalysisDF(r'C:/Users/zuzan/Desktop/MyCompany.xls')
    Competitor1 = CC.AnalysisDF(r'C:/Users/zuzan/Desktop/Competitor.xls')

    Comp0 = pd.concat([Competitor0[list(filter(lambda x: 'tag' in x,  Competitor0.columns))], Competitor0[['q_by_Lp','q_by_Sp']] ] , axis=1)
    Comp1 = pd.concat([Competitor1[list(filter(lambda x: 'tag' in x,  Competitor1.columns))], Competitor1[['q_by_Lp','q_by_Sp']] ] , axis=1)

    Comp0_grouped = Comp0.groupby(list(filter(lambda x: 'tag' in x,  Comp0.columns))).mean().reset_index() 
    Comp1_grouped = Comp1.groupby(list(filter(lambda x: 'tag' in x,  Comp1.columns))).mean().reset_index() 

    TO_dict = {'Threats' : [Competitor1, Comp0_grouped], 'Opportunities':[Competitor0, Comp1_grouped]}
    Threats_and_Opportunities = {}
    for key_ in TO_dict.keys():
        
        _comparison_items =  TO_dict[key_]
        comp_0, comp_1 = _comparison_items[0], _comparison_items[1]

        competition = pd.merge(
                        comp_0,
                        comp_1,
                    on= list(filter(lambda x: 'tag' in x,  CC.common_tags(Competitor0,Comp1_grouped))),
                    how='inner', 
                    suffixes=('_AdvSrch', '_CompAdv'))  

        criteria_advantage_LP = competition['q_by_Lp_AdvSrch'] < competition['q_by_Lp_CompAdv']
        criteria_advantage_SP = competition['q_by_Sp_AdvSrch'] < competition['q_by_Sp_CompAdv']
        
        Advantage_LP = (json.loads(competition[criteria_advantage_LP].to_json(orient="records")))
        Advantage_SP = (json.loads(competition[criteria_advantage_SP].to_json(orient="records")))

        Threats_and_Opportunities[key_] = [{'ListPrices':Advantage_LP},{'StreetPrices':Advantage_SP}]


    return jsonify(Threats_and_Opportunities)


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
