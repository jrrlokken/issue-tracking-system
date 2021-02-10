from unittest import TestCase
from app import app
from models import db, connect_db, User, Issue, Comment, Priority, Status, Category, Role

class DBTests(TestCase):
  ########################
  #### helper methods ####
  ########################
  
  def register(self, email, first_name, last_name, password, confirm):
      return self.app.post(
          '/register',
          data=dict(email=email, first_name=first_name, last_name=last_name, password=password, confirm=confirm),
          follow_redirects=True
      )
  
  def login(self, email, password):
      return self.app.post(
          '/login',
          data=dict(email=email, password=password),
          follow_redirects=False
      )
  
  def logout(self):
      return self.app.get(
          '/logout',
          follow_redirects=True
      )

  def setUp(self):
    app.config['SQLALCHEMY_DATABASE_URI'] = "postgres:///issue_tracker_test"
    app.config['TESTING'] = True
    app.config['DEBUG'] = False
    
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
    response = self.register('user1@example.com', 'User', 'One', 'password', 'password')
    self.assertEqual(response.status_code, 200)

  def test_invalid_registration_email(self):
    response = self.register('user', 'User', 'One', 'password', 'password')
    self.assertIn(b'Invalid email address', response.data)

  def test_registration_passwords_not_matching(self):
    response = self.register('user1@example.com', 'User', 'One', 'password', 'password1')
    self.assertIn(b'Passwords must match', response.data)

  def test_valid_login(self):
    response = self.login('user@example.com', 'password')
    self.assertEqual(200, response.status_code)

  def test_invalid_login(self):
    response = self.login('invaliduser@example.com', 'asdfasdf')
    self.assertIn(b'Invalid email or password', response.data)


