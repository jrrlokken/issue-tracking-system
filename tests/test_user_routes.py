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
		db.session.add_all([ro1,ro2,ro3])
		db.session.commit()

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
  
  # Helper method
	def login(self, email, password):
		return self.client.post(
      '/login',
      data=dict(email=email, password=password),
      follow_redirects = True
		)

	def test_user_root_route_non_admin(self):
		with self.client:
			self.login('testuser1@example.com', 'password')
			response = self.client.get('/users', follow_redirects=True)
			self.assertIn(b'You must be an admin, sorry.', response.data)

	def test_user_root_route_admin(self):
		with self.client:
			self.login('testuser3@example.com', 'password')
			response = self.client.get('/users', follow_redirects=True)
			self.assertIn(b'Users', response.data)
			self.assertIn(b'Test User1', response.data)
			self.assertIn(b'Test User2', response.data)
			self.assertIn(b'Test User3', response.data)

	def test_user_detail_route_non_admin(self):
		with self.client:
			self.login('testuser1@example.com', 'password')
			response = self.client.get('/users/1', follow_redirects=True)
			self.assertIn(b'You must be an admin, sorry.', response.data)
  
	def test_user_detail_route_admin(self):
		with self.client:
			self.login('testuser3@example.com', 'password')
			response = self.client.get('/users/1', follow_redirects=True)
			self.assertIn(b'Test User1', response.data)
			self.assertIn(b'Role: user', response.data)
			self.assertIn(b'EDIT USER', response.data)

	def test_user_edit_route_non_admin(self):
		with self.client:
			self.login('testuser1@example.com', 'password')
			response = self.client.get('/users/1/edit', follow_redirects=True)
			self.assertIn(b'You must be an admin, sorry.', response.data)

	def test_user_edit_route_admin(self):
		with self.client:
			self.login('testuser3@example.com', 'password')
			response = self.client.get('/users/1/edit', follow_redirects=True)
			self.assertIn(b'Edit user Test User1', response.data)
			self.assertIn(b'SAVE', response.data)
			self.assertIn(b'CANCEL', response.data)

	def test_user_delete_route_non_admin(self):
		with self.client:
			self.login('testuser1@example.com', 'password')
			response = self.client.post('/users/1/delete', follow_redirects=True)
			self.assertIn(b'You must be an admin, sorry.', response.data)

	def test_user_delete_route_admin(self):
		with self.client:
			self.login('testuser3@example.com', 'password')
			response = self.client.post('/users/1/delete', follow_redirects=True)
			self.assertIn(b'User Test User1 has been deleted', response.data)