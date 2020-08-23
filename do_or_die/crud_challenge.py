from flask import session, redirect, render_template, request, abort
from bson.objectid import ObjectId
from do_or_die import app, challenges, comments


# CREATE.
@app.route("/create/", methods=["GET", "POST"])
def create():
    if "username" not in session:
        return redirect("/login/")

    if request.method == "POST":
        challenges.insert({"username": session["username"],
                           "description": request.form["description"]})
        return redirect("/mychallenges/")

    return render_template("crud/create.html",
                           title="Create Challenge",
                           username=session["username"])


# READ.
@app.route("/")
@app.route("/challenges/")
def index():
    if "username" not in session:
        return redirect("/login/")

    allChallenges = challenges.find({})
    return render_template("crud/index.html",
                           title="All Challenges",
                           username=session["username"],
                           allChallenges=allChallenges)


@app.route("/mychallenges/")
def myChallenges():
    if "username" not in session:
        return redirect("/login/")

    myChallenges = challenges.find({"username": session["username"]})
    return render_template("crud/mychallenges.html",
                           title="My Challenges",
                           username=session["username"],
                           myChallenges=myChallenges)


@app.route("/challenges/<challengeId>/")
def aChallenge(challengeId):
    if "username" not in session:
        return redirect("/login/")

    aChallenge = challenges.find_one({"_id": ObjectId(challengeId)})
    commentsOfThisChallenge = comments.find({"challengeId": challengeId})
    return render_template("crud/achallenge.html",
                           title="A Challenge",
                           username=session["username"],
                           aChallenge=aChallenge,
                           commentsOfThisChallenge=commentsOfThisChallenge)


# UPDATE.
@app.route("/challenges/<challengeId>/edit/", methods=["GET", "POST"])
def update(challengeId):
    if "username" not in session:
        return redirect("/login/")

    if request.method == "POST":
        aFilter = {"_id": ObjectId(challengeId)}
        anUpdate = {"$set": {"description": request.form["description"]}}
        challenges.update_one(aFilter, anUpdate)
        return redirect("/mychallenges/")

    aChallenge = challenges.find_one({"_id": ObjectId(challengeId)})
    return render_template("crud/edit.html",
                           title="Edit Challenge",
                           username=session["username"],
                           aChallenge=aChallenge)


# DELETE.
@app.route("/challenges/<challengeId>/delete/")
def delete(challengeId):
    if "username" not in session:
        return redirect("/login/")

    aChallenge = challenges.find_one({"_id": ObjectId(challengeId)})
    if session["username"] != aChallenge["username"]:
        abort(404)
    challenges.delete_one({"_id": ObjectId(challengeId)})
    return redirect("/mychallenges/")
