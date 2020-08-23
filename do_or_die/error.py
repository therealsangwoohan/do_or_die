from flask import render_template
from do_or_die import app


@app.errorhandler(404)
def page_not_found(error):
    return render_template("error/404.html", title='404', error=error), 404
