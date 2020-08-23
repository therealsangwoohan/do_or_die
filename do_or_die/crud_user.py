from flask import session, redirect, render_template, abort, request
from do_or_die import app, users


# CREATE.
@app.route("/register/", methods=["POST", "GET"])
def register():
    if request.method == "POST":
        if users.find_one({"name": request.form["username"]}) is None:
            users.insert({"name": request.form["username"],
                          "password": request.form["password"]})
            return redirect("/login/")
    return render_template("auth/register.html", loggedIn=False)


# READ.
@app.route("/login/", methods=["GET", "POST"])
def login():
    if "username" in session:
        abort(404)

    if request.method == "POST":
        login_user = users.find_one({"name": request.form["username"]})
        if login_user is not None:
            if request.form["password"] == login_user["password"]:
                session["username"] = request.form["username"]
                return redirect("/")

    return render_template("auth/login.html", title="Login")


@app.route("/logout/")
def logout():
    if "username" not in session:
        return redirect("/login/")

    del session["username"]
    return redirect("/login/")
