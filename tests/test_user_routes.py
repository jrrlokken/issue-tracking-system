import unittest
from app import app
from models import db, connect_db, User, Role
from flask_login import login_user, logout_user, current_user, login_required

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///issue_tracker_test'
app.config['SQLALCHEMY_ECHO'] = False
app.config['TESTING'] = True
app.config['WTF_CSRF_ENABLED'] = False

connect_db(app)

TEST_USER1 = {
  "email": "testuser1@example.com",
  "first_name": "Test",
  "last_name": "User1",
  "password": "password"
}

TEST_USER2 = {
  "email": "testuser2@example.com",
  "first_name": "Test",
  "last_name": "User2",
  "password": "password"
}

TEST_USER3 = {
  "email": "testuser3@example.com",
  "first_name": "Test",
  "last_name": "User3",
  "password": "password"
}

class UserRouteTests(unittest.TestCase):
	def setUp(self):
		self.client = app.test_client()
		db.drop_all()
		db.create_all()

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

    # Normal user
		user1 = User.register(**TEST_USER1)
    # Assignee user
		user2 = User.register(**TEST_USER2)
    # Admin user
    user3 = User.register(**TEST_USER3)

		user2.role = 1
    user3.role = 2

		db.session.add_all([user1,user2,user3])
		db.session.commit()

  def tearDown(self):
		db.session.remove()
		db.drop_all()