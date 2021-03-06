#! /usr/bin/env python

from flask import sessions, render_template, redirect, Request
from flask import *
import pymongo
from pymongo import MongoClient
import gridfs
from tornado.wsgi import WSGIContainer
from tornado.httpserver import HTTPServer
from tornado.ioloop import IOLoop

# Misc Settings
app = Flask(__name__)
app.secret_key = "\xe0?*\xb3\xcb\x89\x1a[\x12\xa3\xf6v"



# Database Settings
conn = MongoClient('mongodb://localhost:27017/')
db = conn.epolls
fs = gridfs.GridFS(db)


# Home Page
@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        if request.form["fname"] and request.form["matric"] is not None:
            fname = request.form["fname"]
            matric = request.form["matric"]
            exist = db.voters.find_one({"fname": fname, "matric": matric})
            if exist == None:
                import random
                import string
                char_set = string.digits
                token = "%s" % "".join(random.sample(char_set*6, 6)).lower()
                flash("Your token is " + str(token))
                db.voters.insert({"fname": fname, "matric": matric, "token":token, "voted": 0})
                return render_template("index.html", token=token)
            
            elif exist is not None:
                flash("Oopss! You cannot register twice")
                return redirect(url_for("home"))
        else:
            return redirect(url_for("home"))
    elif request.method == "GET":
        return render_template("index.html")



# vote
@app.route("/vote", methods=["GET", "POST"])
def vote():
    if request.method == "POST":
        if request.form["token"] is not None:
            president = request.form["president"]
            vpadmin = request.form["vpadmin"]
            vpacad = request.form["vpacad"]
            welfare = request.form["welfare"]
            software = request.form["software"]
            hardware = request.form["hardware"]
            social = request.form["social"]
            sports = request.form["sports"]
            gensec = request.form["gensec"]
            agensec = request.form["agensec"]
            pro = request.form["pro"]
            treasurer = request.form["treasurer"]
            lr1 = request.form["lr1"]
            lr2 = request.form["lr2"]
            lr3 = request.form["lr3"]
            lr4 = request.form["lr4"]
            token = request.form["token"]
            used = db.voters.find_one({"token": token, "voted": 0})
            cvoted = [president,vpadmin,vpacad,software,hardware,social,sports,gensec,agensec,pro,treasurer,lr1,lr2,lr3,lr4]
            if used is None:
                flash("Token has been used or  is not registered")
                return render_template("vote.html")
            elif used is not None:
                flash("Vote casted successfully...")
                db.voters.update({"token":token}, {"$set":{"voted": 1}})
                db.candidates.update({"init": president}, {"$inc":{"votes": 1}})
                db.candidates.update({"init": vpadmin}, {"$inc":{"votes": 1}})
                db.candidates.update({"init": vpacad}, {"$inc":{"votes": 1}})
                db.candidates.update({"init": welfare}, {"$inc":{"votes": 1}})
                db.candidates.update({"init": software}, {"$inc":{"votes": 1}})
                db.candidates.update({"init": hardware}, {"$inc":{"votes": 1}})
                db.candidates.update({"init": social}, {"$inc":{"votes": 1}})
                db.candidates.update({"init": sports}, {"$inc":{"votes": 1}})
                db.candidates.update({"init": gensec}, {"$inc":{"votes": 1}})
                db.candidates.update({"init": agensec}, {"$inc":{"votes": 1}})
                db.candidates.update({"init": pro}, {"$inc":{"votes": 1}})
                db.candidates.update({"init": treasurer}, {"$inc":{"votes": 1}})
                db.candidates.update({"init": lr1}, {"$inc":{"votes": 1}})
                db.candidates.update({"init": lr2}, {"$inc":{"votes": 1}})
                db.candidates.update({"init": lr3}, {"$inc":{"votes": 1}})
                db.candidates.update({"init": lr4}, {"$inc":{"votes": 1}})
                return render_template("vote.html")
                pass
        else:
            return redirect(url_for("votes"))
    elif request.method == "GET":
        return render_template("vote.html")




@app.route("/results")
def results():
    getAll = list(db.candidates.find())
    p1 = int(getAll[14]["votes"])
    p2 = int(getAll[13]["votes"])
    vpad1 = int(getAll[31]["votes"])
    vpad2 = int(getAll[4]["votes"])
    vpac1 = int(getAll[10]["votes"])
    vpac2 = int(getAll[28]["votes"])
    welf1 = int(getAll[2]["votes"])
    welf2 = int(getAll[6]["votes"])
    return render_template("results.html", p1=p1, p2=p2,\
                           vpad1=vpad1, vpad2=vpad2, \
                           vpac1=vpac1, vpac2=vpac2, \
                           welf1=welf1, welf2=welf2)


@app.route("/results-2")
def results2():
    getAll = list(db.candidates.find())
    soft1 = int(getAll[19]["votes"])
    soft2 = int(getAll[3]["votes"])
    hard1 = int(getAll[9]["votes"])
    hard2 = int(getAll[20]["votes"])
    soc1 = int(getAll[15]["votes"])
    soc2 = int(getAll[22]["votes"])
    spt1 = int(getAll[5]["votes"])
    spt2 = int(getAll[17]["votes"])
    return render_template("results-2.html", soft1=soft1, soft2=soft2,\
                           hard1=hard1, hard2=hard2, \
                           soc1=soc1, soc2=soc2, \
                           spt1=spt1, spt2=spt2)
    

@app.route("/results-3")
def results3():
    getAll = list(db.candidates.find())
    gens1 = int(getAll[27]["votes"])
    gens2 = int(getAll[8]["votes"])
    agens1 = int(getAll[7]["votes"])
    agens2 = int(getAll[12]["votes"])
    pro1 = int(getAll[11]["votes"])
    pro2 = int(getAll[16]["votes"])
    trsr1 = int(getAll[18]["votes"])
    trsr2 = int(getAll[21]["votes"])
    return render_template("results-3.html", gens1=gens1, gens2=gens2,\
                           agens1=agens1, agens2=agens2, \
                           pro1=pro1, pro2=pro2, \
                           trsr1=trsr1, trsr2=trsr2)


@app.route("/results-4")
def results4():
    getAll = list(db.candidates.find())
    lr1a = int(getAll[25]["votes"])
    lr1b = int(getAll[0]["votes"])
    lr2a = int(getAll[30]["votes"])
    lr2b = int(getAll[24]["votes"])
    lr3a = int(getAll[29]["votes"])
    lr3b = int(getAll[26]["votes"])
    lr4a = int(getAll[1]["votes"])
    lr4b = int(getAll[23]["votes"])
    return render_template("results-4.html", lr1a=lr1a, lr1b=lr1b,\
                           lr2a=lr2a, lr2b=lr2b, \
                           lr3a=lr3a, lr3b=lr3b, \
                           lr4a=lr4a, lr4b=lr4b)


@app.route("/team")
def team():
    return render_template("team.html")




if __name__ == '__main__': 
    #app.run(debug=True)
    http_server = HTTPServer(WSGIContainer(app))
    http_server.listen(80)
    IOLoop.instance().start()
