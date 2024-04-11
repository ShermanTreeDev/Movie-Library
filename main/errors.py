from flask import render_template
from werkzeug.exceptions import HTTPException
from main import app, db


@app.errorhandler(404)
def not_found_error(error):
    return render_template('404.html'), 404


@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return render_template('500.html'), 500


@app.errorhandler(HTTPException)
def handle_http_exception(error):
    if error.code == 304:
        db.session.rollback()
        return render_template('304.html'), 304
    return error
