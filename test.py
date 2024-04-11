import os

os.environ['DATABASE_URL'] = 'sqlite://'

import unittest
from main import app, db
from main.models import User, Movie
from flask_login import login_user, logout_user, current_user

class UserModelCase(unittest.TestCase):
    def setUp(self):
        self.app_context = app.app_context()
        self.app_context.push()
        db.create_all()
        self.client = app.test_client(use_cookies=True)  # Ensure cookies are used to maintain session.

        # Create and log in a user
        self.user = User(username='testuser', email='test@example.com')
        db.session.add(self.user)
        db.session.commit()

        # Assuming your application uses Flask-Login and has a login route
        # Replace '/login' with your actual login route and the appropriate form data keys
        response = self.client.post('/login', data={
            'username': 'testuser',
            'password': 'your_test_user_password'  # Ensure this matches the password used when creating the user
        }, follow_redirects=True)

        # Alternatively, directly log in the user with Flask-Login for testing purposes
        # login_user(self.user)

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()
        logout_user()  # Make sure to log out the user after the test

    def test_password_hashing(self):
        u = User(username='susan', email='susan@example.com')
        u.set_password('cat')
        self.assertFalse(u.check_password('dog'))
        self.assertTrue(u.check_password('cat'))

    def test_add_movie_to_collection(self):
        # Create a user and log in
        u = User(username='john', email='john@example.com')
        u.set_password('johnpass')
        db.session.add(u)
        db.session.commit()
        self.client.post('/login', data=dict(username='john', password='johnpass'), follow_redirects=True)

        # Add a movie
        response = self.client.post('/add/Inception', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Movie add successfully!', response.data)

        # Check if the movie is added
        m = Movie.query.filter_by(title='Inception', add_user=u).first()
        self.assertIsNotNone(m)

    def test_delete_movie_from_collection(self):
        # Create a user and log in
        u = User(username='john', email='john@example.com')
        u.set_password('johnpass')
        db.session.add(u)
        db.session.commit()
        self.client.post('/login', data=dict(username='john', password='johnpass'), follow_redirects=True)

        # Add a movie
        m = Movie(title='Inception', add_user=u)
        db.session.add(m)
        db.session.commit()

        # Delete the movie
        response = self.client.post('/delete/Inception', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Movie deleted successfully!', response.data)

        # Check if the movie is deleted
        m = Movie.query.filter_by(title='Inception', add_user=u).first()
        self.assertIsNone(m)

if __name__ == '__main__':
    unittest.main(verbosity=4)
