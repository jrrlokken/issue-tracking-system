import unittest
from app import app
from models import db, connect_db, User, Issue, Comment, Priority, Status, Category, Role
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

class IssueTests(unittest.TestCase):
	def setUp(self):
		self.client = app.test_client()
		db.drop_all()
		db.create_all()

		c1 = Category(
        category_id=0,
        category_label="Technical Issue"
    )

		p1 = Priority(
        priority_id=1,
        priority_label="Medium"
    )

		s1 = Status(
        status_id=0,
        status_label="Submitted"
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

		db.session.add_all([c1,p1,s1,ro1,ro2,ro3])
		db.session.commit()

		User.query.delete()
		Issue.query.delete()

		user1 = User.register(**TEST_USER1)
		user2 = User.register(**TEST_USER2)
		user1.role = 2
		db.session.add_all([user1,user2])
		db.session.commit()

		issue1 = Issue(title="Test Issue 1", text="Issue 1 description", reporter=user1.id)
		issue2 = Issue(title="Test Issue 2", text="Issue 2 description", reporter=user2.id)
		db.session.add_all([issue1,issue2])
		db.session.commit()

		comment1 = Comment(comment_text="This is a comment", comment_user=2, comment_issue=2)
		db.session.add(comment1)
		db.session.commit()

	def tearDown(self):
		db.session.remove()
		db.drop_all()

	def login(self, email, password):
		return self.client.post(
				'/login',
				data=dict(email=email, password=password),
				follow_redirects = True
		)

	def test_new_issue_route_not_logged_in(self):
		with self.client:
			response = self.client.get('/issues/new', follow_redirects=True)
			# self.assertIn(b'Login', response.data)
			self.assertIn(b'Login', response.data)

	def test_new_issue_route_logged_in(self):
		with self.client:
			self.login('testuser1@example.com', 'password')
			response = self.client.get('/issues/new')
			self.assertEqual(200, response.status_code)
			self.assertIn(b'New Issue', response.data)

	def test_issue_detail_route(self):
		with self.client:
			response = self.client.get('/issues/new', follow_redirects=True)
			self.assertIn(b'Login', response.data)

			self.login('testuser1@example.com', 'password')
			response = self.client.get('/issues/1')
			self.assertEqual(200, response.status_code)
			self.assertIn(b'Issue 1 description', response.data)
			self.assertNotIn(b'Issue 2 description', response.data)

	def test_issue_edit_route(self):
		with self.client:
			response = self.client.get('/issues/1/edit', follow_redirects=True)
			self.assertIn(b'Login', response.data)

			self.login('testuser1@example.com', 'password')
			response = self.client.get('/issues/1/edit')
			self.assertEqual(200, response.status_code)
			self.assertIn(b'SAVE', response.data)
			self.assertIn(b'CANCEL', response.data)

	def test_issue_delete_not_logged_in(self):
		with self.client:
			# Not logged in
			response = self.client.post('/issues/1/delete',
			follow_redirects=True)
			self.assertIn(b'Login', response.data)

	def test_issue_delete_non_admin(self):
			self.login('testuser2@example.com', 'password')
			response = self.client.post('/issues/1/delete', follow_redirects=True)
			self.assertIn(b'Admin privileges required', response.data)

	def test_issue_delete_admin_user(self):
			self.login('testuser1@example.com', 'password')
			response = self.client.post('/issues/1/delete', follow_redirects=True)
			self.assertIn(b'has been deleted.', response.data)

	def test_issue_new_comment_route(self):
		with self.client:
			# Not Logged in
			response = self.client.post('/issues/2/comments/new', follow_redirects=True)
			self.assertIn(b'Login', response.data)

			# Logged in, invalid issue
			self.login('testuser2@example.com', 'password')
			response = self.client.post('/issues/3/comments/new', follow_redirects=True)
			self.assertEqual(404, response.status_code)

			# Logged in, valid issue
			# self.login('testuser2@example.com', 'password')
			# response = self.client.post('/issues/2/comments/new', comment_text=(
			# 	"This is a comment"
			# ), follow_redirects=True)
			# self.assertIn(b'This is a comment', response.data)

	def test_comment_delete_route(self):
		with self.client:
			# Not logged in
			response = self.client.post('/comments/1/delete', follow_redirects=True)
			self.assertIn(b'Login', response.data)

	def test_comment_delete_non_admin(self):
			self.login('testuser2@example.com', 'password')
			response = self.client.post('/comments/1/delete', follow_redirects=True)
			self.assertIn(b'Admin privileges required', response.data)

	def test_comment_delete_admin_user(self):
			self.login('testuser1@example.com', 'password')
			response = self.client.post('/comments/1/delete', follow_redirects=True)
			self.assertIn(b'Comment #1 has been deleted.', response.data)