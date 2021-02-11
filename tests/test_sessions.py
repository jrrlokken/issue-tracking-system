from unittest import TestCase
from app import app
from models import db, connect_db, User, Issue, Comment, Priority, Status, Category, Role
from flask_login import login_user, logout_user, current_user, login_required

class DBUserTests(TestCase):
  ########################
  #### helper methods ####
  ########################
  
  def register(self, email, first_name, last_name, password, confirm):
      return self.app.post(
          '/register',
          data=dict(email=email, first_name=first_name, last_name=last_name, password=password, confirm=confirm),
          follow_redirects = True
      )
  
  def login(self, email, password):
      return self.app.post(
          '/login',
          data=dict(email=email, password=password),
          follow_redirects = False
      )
  
  def logout(self):
      return self.app.get(
          '/logout',
          follow_redirects = True
      )

  def setUp(self):
    app.config['SQLALCHEMY_DATABASE_URI'] = "postgres:///issue_tracker_test"
    app.config['TESTING'] = True
    self.app = app.test_client()

    db.drop_all()
    db.create_all()

    ro1 = Role(
      role_id=0,
      role_label="user"
    )
    db.session.add(ro1)
    db.session.commit()

    user = User.register('user@example.com', 'Test', 'User', 'password')
    db.session.add(user)
    db.session.commit()

  def tearDown(self):
    db.session.remove()
    db.drop_all()

  def test_valid_user_registration(self):
    response = User.register('user1@example.com', 'User', 'One', 'password')

  def test_invalid_registration_email(self):
    response = self.register('user', 'User', 'One', 'password')
    self.assertIn(b'Invalid email address', response.data)




