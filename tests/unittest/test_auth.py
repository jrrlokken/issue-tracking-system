import unittest
from app import app
from models import db, connect_db, User, Issue, Comment, Priority, Status, Category, Role
from flask_login import login_user, logout_user, current_user, login_required

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///issue_tracker_test'
app.config['SQLALCHEMY_ECHO'] = False
app.config['TESTING'] = True
app.config['WTF_CSRF_ENABLED'] = False

connect_db(app)

TEST_USER = {
  "email": "testuser@example.com",
  "first_name": "Test",
  "last_name": "User",
  "password": "password"
}

class AuthTests(unittest.TestCase):
  def setUp(self):
    self.client = app.test_client()
    db.drop_all()
    db.create_all()

    p1 = Priority(
        priority_id=0,
        priority_label="Low"
    )

    p2 = Priority(
        priority_id=1,
        priority_label="Medium"
    )

    p3 = Priority(
        priority_id=2,
        priority_label="High"
    )

    p4 = Priority(
        priority_id=3,
        priority_label="Urgent"
    )

    # Status

    s1 = Status(
        status_id=0,
        status_label="Submitted"
    )

    s2 = Status(
        status_id=1,
        status_label="Assigned"
    )

    s3 = Status(
        status_id=2,
        status_label="Resolved"
    )

    # Category

    c1 = Category(
        category_id=0,
        category_label="Technical Issue"
    )

    c2 = Category(
        category_id=1,
        category_label="Customer Complaint"
    )

    c3 = Category(
        category_id=2,
        category_label="Product Request"
    )

    ro1 = Role(
        role_id=0,
        role_label="user"
    )

    ro2 = Role(
        role_id=1,
        role_label="assignee"
    )

    ro3 = Role(
        role_id=2,
        role_label="admin"
    )

    db.session.add_all([p1,p2,p3,p4,s1,s2,s3,c1,c2,c3,ro1,ro2,ro3])
    db.session.commit()

    User.query.delete()
    Issue.query.delete()

    user = User.register(**TEST_USER)
    db.session.add(user)
    db.session.commit()

    issue = Issue(title="Test Issue", text="Issue description", reporter=user.id)
    db.session.add(issue)
    db.session.commit()
  
  def tearDown(self):
    db.session.remove()
    db.drop_all()

  ########################
  #### helper methods ####
  ########################
  
  def register(self, email, first_name, last_name, password, confirm):
      return self.client.post(
          '/register',
          data=dict(email=email, first_name=first_name, last_name=last_name, password=password, confirm=confirm),
          follow_redirects = True
      )
  
  def login(self, email, password):
      return self.client.post(
          '/login',
          data=dict(email=email, password=password),
          follow_redirects = True
      )
  
  def logout(self):
      return self.client.get(
          '/logout',
          follow_redirects = True
      )

  ###############
  #### tests ####
  ###############

  def test_valid_user_registration(self):
    response = self.register('user@example.com', 'Test', 'User', 'password', 'password')
    self.assertIn(b'New Issue', response.data)
    self.assertEqual(200, response.status_code)
  
  def test_user_registration_duplicate_email(self):
    response = self.register('testuser@example.com', 'Test', 'User', 'password', 'password')
    self.assertIn(b'testuser@example.com has already been registered', response.data)

  def test_registration_messages(self):
    """Test registration validation messages."""
    response = self.register('user1@example.com', 'User', 'One', 'cat', 'cat')
    self.assertIn(b'Field must be between 8 and 32 characters long.', response.data)

    response = self.register('user', 'User', 'One', 'password', 'password')
    self.assertIn(b'Invalid email address', response.data)

  def test_valid_login(self):
    response = self.login('testuser@example.com', 'password')
    self.assertIn(b'Test Issue', response.data)
    self.assertIn(b'Issue description', response.data)

  def test_invalid_login(self):
    response = self.login('user@example.com', 'password')
    self.assertIn(b'Invalid email or password', response.data)

  def test_logout(self):
    response = self.logout()
    self.assertNotIn(b'Test Issue', response.data)

  # Miscellaneous routes
  def test_search_route(self):
    """Test /search route."""
    self.login('testuser@example.com', 'password')
    response = self.client.get('/search?search=issue')
    self.assertIn(b'Test Issue', response.data)

if __name__ == "__main__":
  unittest.main()