import sys
import os
from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session, url_for, flash
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash
from sqlite3 import IntegrityError
from datetime import datetime
import pytz
from helpers import apology, login_required, usd


# Configure application
app = Flask(__name__)
app.secret_key = os.urandom(16)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True


# Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


# Custom filter
app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///db.db")


tehran = pytz.timezone('Asia/Tehran')
tehran_time = datetime.now(tehran)

@app.route("/")
@login_required
def index():
    """Show portfolio of stocks"""

    id = session["id"]
    row = db.execute("SELECT * FROM users WHERE id = ?", id)
    Fname = row[0]['Fname']
    Lname = row[0]['Lname']
    if request.method == 'POST':        
        button_pressed = request.form.get('button_action')        
        if button_pressed == 'button4':
                pipelines = session.get('Pipeliness')
                return redirect(url_for('pipelines', Pipes=pipelines))
        elif button_pressed == 'button6':
            print("i am here")
            return redirect("/trans_control")

    return render_template("index.html", Fname=Fname, Lname=Lname)


@app.route("/login", methods=["GET", "POST"])
def login():
    error = None
    """Log user in"""
    
    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        try:
            rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))
            session["id"] = rows[0]["id"]
        except IndexError:
            return apology("\nusername not found!", 403)

        if rows[0]["passwort"] != request.form.get("password"):
            error = 'Invalid username or password'

        else:
            return redirect("/")

    return render_template("login.html", error=error)


    #     # Ensure username was submitted
    #     if not request.form.get("username"):
    #         return apology("Please enter a username", 403)

    #     # Ensure password was submitted
    #     elif not request.form.get("password"):
    #         return apology("Please enter a password", 403)

    #     # Query database for username
    #     rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))

    #     # Ensure username exists and password is correct
    #     if len(rows) != 1 or rows[0]["passwort"] != request.form.get("password"):
    #         return apology("Username and/or password are/is invalid", 403)

    #     # Remember which user has logged in
    #     session["id"] = rows[0]["id"]

    #     # Redirect user to home page
    #     return redirect("/")

    # # User reached route via GET (as by clicking a link or via redirect)
    # else:
    #     return render_template("login.html")



@app.route("/pipelines", methods=["GET", "POST"])
@login_required
def pipelines():
    user_id = session["id"]
    button_pressed = request.form.get('button_action')
    if button_pressed == 'button3':
    # if request.method == "POST":
        pipename = request.form.get("pipelines")
        user_id = session["id"]

        try:
            db.execute("INSERT INTO father (user_id, pipname) VALUES (?, ?)", user_id, pipename)
        except ValueError:
            return apology("\npipename already exists. \nPlease choose a different pipename.", 403)
    Pipelines = db.execute("SELECT id, pipname FROM father WHERE pipname IS NOT NULL AND user_id = ? ORDER BY id DESC", user_id)
    session["Pipeliness"] = Pipelines
    return render_template("pipelines.html", Pipes=Pipelines)

# def redirect_to_pipe():
#     if request.method == "POST":
#         # data = request.get_json()
#         # id = data['id']
#         return redirect(url_for('pipeline', id=id))

@app.route("/pipeline/<int:id>", methods=["GET", "POST"])
@login_required
def pipeline(id):
    id_ = id
    session['pipeid'] = id
    user_id = session["id"]
    name = db.execute("SELECT pipname FROM father WHERE id = ?", id_)
    button_pressed = request.form.get('button_action')
    items = session.get('ch2')
    station_id = items
    # Lcheck  = db.execute("SELECT time, date, potential FROM baby WHERE date != 'YYYY-MM-DD' AND baby_station = ? ORDER BY date DESC LIMIT 1", station)

    # Lcheck=[]
    # items_id = session.get('ch2')

    if button_pressed == 'button1':
        station = request.form.get("station")
        consideration = request.form.get("consideration")
        db.execute("INSERT INTO kid (user_id, kid_id, station, consideration) VALUES (?, ?, ?, ?)", user_id, id_,  station, consideration)



    st_list = db.execute("SELECT id, station, consideration FROM kid WHERE station IS NOT NULL AND kid_id = ? ORDER BY id DESC", id_)
    choomche = db.execute("SELECT baby_station, id, potential, date, time FROM baby WHERE baby_id = ? ORDER BY date DESC, time DESC", id_)
    # WHERE baby_id = ?, kid_id

        #  برای نمایش آخرین وضعیت در قسمت پایپلاین
    # if "stationid" in session:
    #     id__s = session["stationid"]
    #     choomche = db.execute("SELECT baby_station, id, potential, date, time FROM baby WHERE id = ? ORDER BY date, time DESC", id__s)
    # else:
    #     choomche = []
    # choom = session['id_station']
    return render_template("pipeline.html", id_show=name, id=id_, sts=st_list, lcheck=station_id, items=choomche)

@app.route("/station/<int:id>", methods=["GET", "POST"])
@login_required
def station(id):
    id_ = id
    kid_id = session['pipeid']
    session["stationid"] = id
    user_id = session["id"]
    name = db.execute("SELECT id, station FROM kid WHERE id = ?", id_)


    button_pressed = request.form.get('button_action')
    if button_pressed == 'button2':
        # print(kid_id)
        consideration = request.form.get("consideration")
        voltage = request.form.get("voltage")
        data = request.form.get("data")
        time = request.form.get("time")
        db.execute("INSERT INTO baby (baby_id, id, user_id, consideration, baby_station, potential, date, time) VALUES (?, ?, ?, ?, ?, ?, ?, ?)", kid_id , id_ , user_id, consideration, name[0]["station"], voltage, data, time)



    checkes = db.execute("SELECT id, user_id, consideration, baby_station, potential, date, time FROM baby WHERE id = ? ORDER BY date DESC", id_)

    choom = db.execute("SELECT id_check FROM baby WHERE id = ? ORDER BY date DESC", id_)

    #  برای نمایش آخرین وضعیت در قسمت پایپلاین
    # session['id_station'] = choom
    # print(type(checkes[0]["id"]))
    # session['id_station'] = checkes[0]["id"]
    # if 'ch1' in session:
    #     items = session['ch1']
    # checkes_id = db.execute("SELECT id FROM baby WHERE id = ? ORDER BY date DESC", items)
    # session['ch2'] = checkes_id

    return render_template("station.html", id_show=name, id__=id_, checkes=checkes, items=choom)


@app.route('/your_flask_endpoint', methods=['POST'])
def receive_data():
    data = request.json  # This will contain the content of <li> elements as a list
    print(data)
    pipeid = session.get('pipeid')
    name = db.execute("SELECT pipname FROM father WHERE id = ?", pipeid)
    session['ch1'] = data

    # return redirect(url_for('pipeline', id_show=name, id=pipeid, items=data))
    return render_template("pipeline.html", id_show=name, id=pipeid, items=data)

#برای ایجاد و کنترل صفحع کنترل ترانسها 
@app.route('/trans_control' , methods = ['POST','GET'])
@login_required
def trans_control():
    translist = []
    current_time = datetime.now()
    id_draft = db.execute("select DISTINCT id from Trans_rectifire")
    if id_draft:
        for i in id_draft : 
            newlist = db.execute("select id,VOLTAGE,Current from Trans_rectifire where id =? order by date DESC", i["id"])
            translist.append(newlist[0])
    
    if request.method == 'POST':
        btn = request.form.get("btn-info")
        if btn is not None:        
            return redirect('/trans_info?btn=' + btn)        
    return render_template("transes.html", trans_list = translist, now = current_time)                                       
        
@app.route('/trans_info' , methods = ['POST','GET'])
@login_required
def trans_info():
    current_time = datetime.now()
    btn = request.args.get("btn")
    user = db.execute("select Fname,Lname from users where id = ?" , session["id"])
    current_user = user[0]['Fname'] +" " +  user[0]['Lname']
    id = btn
    listy = db.execute("select * from Trans_rectifire where id =? order by date DESC", id)
    for i in listy:
        username = db.execute("select Fname,Lname from users where id = ?" , i['user_id'])
        i['username'] = username[0]['Fname'] +" " + username[0]['Lname']            

    if request.method == "POST":                    
        #try:
        id = request.form.get("trans-id")
        voltage = request.form.get("Voltage")
        current = request.form.get("Current")
        oil = request.form.get("oil")
        temperature = request.form.get("temperature")
        geo_location = request.form.get("GeoLocation")            
        timestamp = request.form.get("Timestamp")                           
        db.execute("insert into Trans_rectifire (id,user_id,geolocation,Current,VOLTAGE,temprature,oil,date) values(?,?,?,?,?,?,?,?)" , 
                    id,session["id"],geo_location,current,voltage,temperature,oil,timestamp)
        return redirect('/trans_info?btn=' + str(id) )                        
    return render_template("onetranses.html" , trans_data = listy, user = current_user, id= id, now = current_time)

@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("login")
    # return render_template("two.html", items=data)

    # station = request.form.get('station')
    # if not station:
    #     # station = "default_station"
    #     # db.execute("INSERT INTO baby (user_id, baby_station, potential, date, time) VALUES (?, ?, ?, ?, ?)", user_id, station, 0, "YYYY-MM-DD", "HH:MM:SS")
    #     Lcheck = []

        # db.execute("SELECT time, date, potential FROM baby WHERE date != 'YYYY-MM-DD' AND baby_station = ? ORDER BY date DESC LIMIT 1", station)


    # if request.method == "POST":
            # baby_id = db.execute("SELECT id FROM baby WHERE baby_station = ?", station)

        # db.execute("INSERT INTO baby (user_id, baby_station, potential, date, time) VALUES (?, ?, ?, ?, ?)", user_id, station, 0, "YYYY-MM-DD", "HH:MM:SS")
        # Lcheck  = db.execute("SELECT * FROM baby WHERE date != 'YYYY-MM-DD' AND baby_station = ? ORDER BY date DESC LIMIT 1", station)

    # if button_pressed == 'button2':
    # Lcheck  = db.execute("SELECT * FROM baby WHERE date != 'YYYY-MM-DD' AND baby_station = ? ORDER BY date DESC LIMIT 1", station)
