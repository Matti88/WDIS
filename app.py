

import Conf_Calculator as CC
import Conf_Checker as CChe
import os 
from flask import (Flask, 
            jsonify, request, render_template
            , make_response, redirect, url_for
            ,send_from_directory, current_app
            ) 
from flask_jwt_extended import (
    get_jwt_identity,
    JWTManager, jwt_required, create_access_token,
    jwt_refresh_token_required, create_refresh_token,
    get_jwt_identity, set_access_cookies,
    set_refresh_cookies, unset_jwt_cookies 
    )
import sqlite3 as sql3
import json
from sys import platform as _platform
isLinuzSystem = True
if _platform == "linux" or _platform == "linux2":
    print(_platform)
    isLinuzSystem = True
else:
    print(_platform)
    isLinuzSystem = True 


app = Flask(__name__)
app.config['RESULT_STATIC_PATH'] = "results/"


# Configure application to store JWTs in cookies
app.config['JWT_TOKEN_LOCATION'] = ['cookies']

# Only allow JWT cookies to be sent over https. In production, this
# should likely be True
app.config['JWT_COOKIE_SECURE'] = False

# Set the cookie paths, so that you are only sending your access token
# cookie to the access endpoints, and only sending your refresh token
app.config['JWT_ACCESS_COOKIE_PATH'] = '/checker'
app.config['JWT_REFRESH_COOKIE_PATH'] = '/token/refresh'
app.config['JWT_COOKIE_CSRF_PROTECT'] = True

# Set the secret key to sign the JWTs with
app.config['JWT_SECRET_KEY'] = 'super-secret'  # Change this!
jwt = JWTManager(app)

#address with values for the uploads and types of files
if isLinuzSystem:
    app.config["OCpR_file_UPLOADS"] = "./uploads"
else:
    app.config["OCpR_file_UPLOADS"] = ".\\uploads"
app.config["ALLOWED_OCpR_file_EXTENSIONS"] = ["XLSX", "XLS"]

    
#Utility Functions
def allowed_image(filename):
    if not "." in filename:
        return False
    ext = filename.rsplit(".", 1)[1]
    if ext.upper() in app.config["ALLOWED_OCpR_file_EXTENSIONS"]:
        return True
    else:
        return False



# JWT APIs
@app.route('/login', methods=['POST'])
def login():
    username = request.json.get('login', None)
    password = request.json.get('password', None)
 
    conn = sql3.connect('accounts.db')
    c = conn.cursor()
    t = (username,)

    # Create the tokens we will be sending back to the user
    access_token = create_access_token(identity=username)
    refresh_token = create_refresh_token(identity=username)

    # Set the JWTs and the CSRF double submit protection cookies
    # in this response
    c.execute('SELECT * FROM users WHERE User=?', t)
    answers = c.fetchone()
    if username == answers[0] and password == answers[0]:
        conn.close()
        resp = jsonify({'login': True})
        set_access_cookies(resp, access_token)
        set_refresh_cookies(resp, refresh_token)
        return resp, 200
    else:
        conn.close()
        return jsonify({'login': False}), 401


@app.route('/token/refresh', methods=['POST'])
@jwt_refresh_token_required
def refresh():
    # Create the new access token
    current_user = get_jwt_identity()
    access_token = create_access_token(identity=current_user)
    resp = jsonify({'refresh': True})
    set_access_cookies(resp, access_token)
    return resp, 200

@app.route('/token/remove', methods=['POST'])
def logout():
    resp = jsonify({'logout': True})
    unset_jwt_cookies(resp)
    return resp, 200


#Main View
@app.route('/results/<path:filename>')
def serve_static(filename):
    if filename.endswith("index.html"):
        return send_from_directory("results/",  "login.html")
    else:
        return send_from_directory("results/", filename)
 
   

#api for the analysis 
@app.route("/checker/advantages", methods=["GET"])
@jwt_required
def advantages():
    MyCompany_   = request.args['MyCompany']
    Competitor_  = request.args['Competitor']
    print("Processing advantages with files of: " ,  MyCompany_, ' and ', Competitor_)
    if isLinuzSystem:
        return jsonify(CC.AdvantageDisadvantageCal(MyCompany='./uploads/' + MyCompany_, Competitor='./uploads/' + Competitor_))
    else:
        return jsonify(CC.AdvantageDisadvantageCal(MyCompany='.\\uploads\\' + MyCompany_, Competitor='.\\uploads\\' + Competitor_))

@app.route("/checker/confronts", methods=["GET"])
@jwt_required
def Product_on_confrontation():
    MyCompany_   = request.args['MyCompany']
    Competitor_  = request.args['Competitor']
    print("Processing confrontations with files of: " ,MyCompany_, ' and ', Competitor_)
    if isLinuzSystem:
        return jsonify(CC.Product_on_confrontation(MyCompany='./uploads/' + MyCompany_, Competitor='./uploads/' + Competitor_))
    else:
        return jsonify(CC.Product_on_confrontation(MyCompany='.\\uploads\\' + MyCompany_, Competitor='.\\uploads\\' + Competitor_))

 

@app.route("/checker/competitveness", methods=["GET"])
@jwt_required
def competitveness():
    return jsonify(CC.ThreatsOpportunitiesCal())

@app.route("/checker/sales_analysis", methods=["GET"])
@jwt_required
def sales_analysis():
    MyCompany_   = request.args['MyCompany']
    Competitor_  = request.args['Competitor']
    print("Processing sales analysis with files of: " , MyCompany_, ' and ', Competitor_)
    if isLinuzSystem:
        return jsonify(CC.sales_analysis_gen_matcher(MyCompany='./uploads/' + MyCompany_, Competitor='./uploads/' + Competitor_))
    else:
        return jsonify( CC.sales_analysis_gen_matcher(MyCompany='.\\uploads\\' + MyCompany_, Competitor='.\\uploads\\' + Competitor_) )

    

@app.route("/checker/Checker_OCpR_file", methods=["GET"])
@jwt_required
def Checker_OCpR():
    data = None
    filename = request.headers['Side']
    print(filename)
    if request.method == "GET":
        if isLinuzSystem:
            data = CChe.comb_estimator('./uploads/' + filename)
        else:
            data = CChe.comb_estimator('.\\uploads\\' + filename)
    return data

@app.route("/checker/SaveAnalysis", methods=["POST"])
@jwt_required
def SaveAnalysis():
    dict_of_savedAnalysis = request.json
    Username_      = dict_of_savedAnalysis['Username']
    #Possibly to change it to this item
    indetity =get_jwt_identity() 
    saved_analysis_ = dict_of_savedAnalysis['analysis']  
 
    try:
        if isLinuzSystem:
            conn = sql3.connect('./accounts.db')
        else:
            conn = sql3.connect('.\\accounts.db')
        c = conn.cursor()
        saved_analysis = json.dumps(saved_analysis_)
        values = ( saved_analysis, Username_)
        sql = ''' UPDATE analysis SET storedAnalisys = ? where User= ?'''
        c.execute(sql, values)
        conn.commit()
        conn.close()
        return jsonify({'update':"correct" })
    except:
        return jsonify({'update':"not_correct" })


@app.route("/checker/RetrievedSavedAnalysis", methods=["GET"])
@jwt_required
def RetrievedSavedAnalysis():
    indetity =get_jwt_identity() 
    print(indetity)  
 
    try:
        if isLinuzSystem:
            conn = sql3.connect('./accounts.db')
        else:
            conn = sql3.connect('.\\accounts.db')
        c = conn.cursor()
        values = ( indetity, )
        sql = ''' select storedAnalisys from analysis where User= ?'''
        c.execute(sql, values)
        saved_analysis = c.fetchone()[0]
        conn.close()
        return saved_analysis
    except:
        return jsonify({  indetity: "error"})
    

@app.route("/ListStreet", methods=["GET"])
@jwt_required
def ListStreet():
    if request.method == "GET":
        name_of_the_file = request.args.get('fileName')
        if isLinuzSystem:
            file_ = os.getcwd() + r"/uploads" + '/' + name_of_the_file 
        else:
            file_ = os.getcwd() + r"\uploads" + '\\' + name_of_the_file 

        resultForChartJS = CC.ListStreetCal(file_, D3_ChartJS = False)
    return jsonify(resultForChartJS)





@app.route("/checker/upload-OCpR_file", methods=["GET", "POST"])
def upload_OCpR_file():
    if request.method == "POST":
        if request.headers['Side'] == 'MyCompany':
            print("adding this file to MyCompany Side")
        elif request.headers['Side'] == 'Competitor':
            print("adding this file to Competitor Side") 
            
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

#favicon
@app.route('/favicon.ico')
def favicon():
    return send_from_directory("results/", 'favicon.ico')


if __name__ == '__main__':
    print("This is a standard FUCK YOU!")
    app.run()