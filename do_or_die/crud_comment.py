from flask import session, redirect, request, abort
from bson.objectid import ObjectId
from do_or_die import app, comments


# CREATE.
@app.route("/challenges/<challengeId>/comments/addcomment/", methods=["POST"])
def addComment(challengeId):
    if "username" not in session:
        return redirect("/login/")

    comments.insert({"challengeId": challengeId,
                     "username": session["username"],
                     "raw": request.form["raw"]})
    return redirect(f"/challenges/{challengeId}/")


# DELETE.
@app.route("/challenges/<challengeId>/<commentId>/delete/")
def deleteComment(challengeId, commentId):
    if "username" not in session:
        return redirect("/login/")

    aComment = comments.find_one({"_id": ObjectId(commentId)})
    if session["username"] != aComment["username"]:
        print(session["username"])
        print(aComment["username"])
        abort(404)
    comments.delete_one({"_id": ObjectId(commentId)})
    return redirect(f"/challenges/{challengeId}/")
