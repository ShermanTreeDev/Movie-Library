import sqlalchemy as sa
import sqlalchemy.orm as so
from main import app, db
from main.models import User, Movie


@app.shell_context_processor
def make_shell_context():
    return {'sa': sa, 'so': so, 'db': db, 'User': User, 'Movie': Movie}