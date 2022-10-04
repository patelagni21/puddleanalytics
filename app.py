#!/usr/bin/env python3
import mpu.aws
import sys
import requests
import mpu
import boto3
import flask
from flask import Flask, render_template, request, session, g, redirect
import pygal
import json
import time
import revenue_by_product
import quarter_rev
import month_rev
import revenue_by_region
import year_rev
import revenue_by_product_radar
import average_sales_per_month
import quarter_gauge_benchmark
import os
from flask import Flask, render_template, request, redirect, send_file, url_for
from s3_demo import list_files, download_file, upload_file
from queue import Queue
import optimizing
import multiprocessing
from flask.helpers import make_response, url_for
from flask_login.utils import login_user
import config
import login, authorization

from urllib.parse import urlparse, urljoin

def is_safe_url(target):
    ref_url = urlparse(request.host_url)
    test_url = urlparse(urljoin(request.host_url, target))
    return test_url.scheme in ('http', 'https') and \
           ref_url.netloc == test_url.netloc

aws_access_key=config.__AWS_ACCESS_KEY
_AWS_SECRET_ACCESS_KEY=config.__AWS_SECRET_ACCESS_KEY

app = Flask(__name__)
app.secret_key = "__SECRET_KEY"

app.config["MONGO_URI"] = config.__MONGODB_URL

User = login.User

login_manager = login.Login(app)
login_manager.session_protection = "strong"

auth = authorization.Auth(app)
sess = authorization.Sessions(app)
UPLOAD_FOLDER = "uploads"
BUCKET = "puddlebucket"
TEST_BUCKET='s3://puddlebucket/'

@app.before_request
def before_request():
    g.user = None

    session.pop('_flashes', None)

    if '_sessionId' in session:
        user = sess.getUserFromSession(session["_sessionId"])
        if user:
            g.user = User(user)
        else:
            print("session id has expired")
            session.pop('_sessionId',None)

@app.route("/home/<filename>", methods=['GET'])
def home(filename):
    print(filename)
    filename = filename.split('_', 1)
    byte_file=s3_read(TEST_BUCKET+filename)
    string_file=byte_file.decode('ISO-8859-1')
    if sys.version_info[0] < 3:
        from StringIO import StringIO
    else:
        from io import StringIO

    TESTDATA=StringIO(string_file)
    file_input=TESTDATA.read()
    if not "_sessionId" in session:
        return flask.redirect(url_for('login'))
    else:
        jobs = Queue()
        jobs.put(['prod_rev', revenue_by_product.revenue_by_product(file_input), 'static/images/rev_by_product_chart.svg'])

        jobs.put(['quarter_rev', quarter_rev.quarter_rev(file_input), 'static/images/quarter_rev_chart.svg'])
        jobs.put(['month_rev', month_rev.month_rev(file_input), 'static/images/month_rev_chart.svg'])
        jobs.put(['region_rev', revenue_by_region.revenue_by_region(file_input), 'static/images/region_rev_chart.svg'])
        jobs.put(['year_rev', year_rev.year_rev(file_input), 'static/images/year_rev_chart.svg'])
        jobs.put(['radar_prod_rev', revenue_by_product_radar.revenue_by_product_radar(file_input), 'static/images/rev_by_product_radar_chart.svg'])
        jobs.put(['avg_sales_per_month_rev', average_sales_per_month.average_sales_per_month(file_input), 'static/images/avg_sales_per_month_rev_chart.svg'])

        
        # manager = multiprocessing.Manager()
        # output = manager.dict()
        # numtasks = jobs.qsize()

        # start = time.time()
        # processes = []
        # for i in range(numtasks):
        #     proc = multiprocessing.Process(target=optimizing.mp_Worker, args=(i, jobs.get(), output))
        #     processes.append(proc)
        #     proc.start()
        #     #worker = optimizing.Multithreading(jobs, output, i)
        #     #worker.daemon = True
        #     #worker.start()

        # print(f"waiting for {numtasks} jobs to finish.")
        # for proc in processes:
        #     proc.join()

        # print(output)
        # elapsed = time.time() - start
        # print(f"Finished all tasks after {elapsed}")
        output = {}
        numtasks = jobs.qsize() 

        start = time.time()

        for i in range(100):
                if jobs.empty(): break
                worker = optimizing.Worker(jobs, output, i)
                worker.daemon = True
                worker.start()

        print(f"waiting for {numtasks} jobs to finish.")
        jobs.join()

        print(f"Elapsed time: {time.time()-start}")

        print(output)
        
        return render_template(
            'app.html',
            chart_name1 = 'Revenue by Product Radar Graph(in %)', image1_url = output['radar_prod_rev'],
            chart_name2 = 'Revenue by Quarter', image2_url = output['quarter_rev'],
            chart_name3 = 'Revenue by Month', image3_url = output['month_rev'],
            chart_name4 = 'Revenue by Region', image4_url = output['region_rev'],
            chart_name5 = 'Revenue by Year', image5_url = output['year_rev'],
            chart_name6 = 'Revenue by Product (in %)',image6_url = output['prod_rev'],
            chart_name7 = 'Revenue by Year', image7_url = output['avg_sales_per_month_rev']
        )

@app.route("/calculator")
def test():
    return render_template('calculator.html')

@app.route("/login", methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        session.pop("_sessionId",None)

        email, password = request.form.get('email'), request.form.get('password')

        user = auth.get_user(email)
        if user != None and auth.validate_user(user, password):
            __SESSION_ID = sess.newSession(user['_id'])
            session['_sessionId'] = __SESSION_ID

            g.user = User(user)

            flask.flash(f"Logged in successfully.")

            next = flask.request.args.get('next')
            if not is_safe_url(next):
                return flask.abort(400)
            
            return redirect("/settings")
        else:

            flask.flash("Could not find user with these credentials.")
    return render_template('login.html', error=error)

@app.route('/logout',methods=['GET'])
def logout():
    if g.user != None:
        print(g.user)

        sess.deleteSession(session["_sessionId"])

        g.user = None

        session.pop("_sessionId",None)

        flask.flash("Logged out.")

    return flask.redirect(url_for("login"))

# @app.route("/test")
# def test():
#     return render_template('base.html')
# @app.route("/settings")
# def settings():
#     if not "_sessionId" in session:
#         return flask.redirect(url_for('login'))
#     return render_template('settings.html')

@app.route("/settings")
@app.route("/")
def storage():
    if not "_sessionId" in session:
        return flask.redirect(url_for('login'))

    contents = list_files(BUCKET,filter=g.user.id+"_")#, filter=(g.user.id+"_"))
    newContents=[]

    # print("display content for",g.user.id)
    # print(contents)

    for content in contents:
        # print("a",content.key)
        # file_params = content.get("Key").split("_",1)
        # content["displayName"] = file_params[1]
        # newContents.append(content)
        newContents.append({"displayName":content.key.split("_",1)[1], "Key":content.key})
    return render_template('settings.html', contents=newContents)


@app.route("/upload", methods=['POST'])
def upload():

    user = sess.getUserFromSession(session["_sessionId"])

    if user and request.method == "POST":
        f = request.files['file']

        if not ('.' in f.filename and \
           f.filename.rsplit('.', 1)[1].lower() == "csv"):
           return make_response({"message":"File failed to upload"},400)
        
        g.user = User(user)

        f.save(f.filename)
        upload_file(f"{f.filename}", BUCKET,g.user.id)



        return redirect("/settings")

def s3_read(source, profile_name=None):
    session= boto3.Session(aws_access_key_id=aws_access_key, aws_secret_access_key=_AWS_SECRET_ACCESS_KEY)
    s3=session.client('s3')
    bucket_name, key=mpu.aws._s3_path_split(source)
    s3_object=s3.get_object(Bucket=bucket_name, Key='sales_data_sample.csv')
    print(s3_object)
    body=s3_object['Body']
    return body.read()





@app.route("/download/<filename>", methods=['GET'])
def download(filename):
    
    return redirect(url_for("home", filename))





    



    

    


@app.route("/register", methods=['GET', 'POST'])
def register():
    error = None
    if request.method == 'POST':
        session.pop("_sessionId",None)

        email, password = request.form.get('email'), request.form.get('password')

        user = auth.get_user(email)
        if user == None:
            auth.registerUser(email, password)

            user = auth.get_user(email)
            
            __SESSION_ID = sess.newSession(user['_id'])
            session['_sessionId'] = __SESSION_ID
            
            g.user = User(user)
            
            return flask.redirect(url_for('settings'))

        else:

            flask.flash("Email already registered.")
    
    return render_template('register.html', error=error)



if __name__ == '__main__':
    app.run(debug=True)
