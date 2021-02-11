import unittest
from app import app


class RenderTests(unittest.TestCase):
  """Test each route for proper render."""
  def setUp(self):
    app.config['TESTING'] = True
    app.config['DEBUG'] = False
    self.client = app.test_client()

  def test_homepage(self):
    """Test root route."""
    with self.client:
      response = self.client.get('/')
      self.assertIn(b'Welcome to ITS', response.data)
      self.assertEqual(200, response.status_code)

  def test_register_route(self):
    """Test /register route."""
    with self.client:
      response = self.client.get('/register')
      self.assertIn(b'Register for an account', response.data)
      self.assertEqual(200, response.status_code)


  def test_login_route(self):
    """Test /login route."""
    with self.client:
      response = self.client.get('/login')
      self.assertIn(b'Login', response.data)
      self.assertEqual(200, response.status_code)


  def test_logout_route(self):
    """Test /logout route."""
    with self.client:
      response = self.client.get('/logout')
      self.assertEqual(302, response.status_code)

  def test_404_route(self):
    """Test the 404 handler."""
    with self.client:
      response = self.client.get('/blargh')
      self.assertIn(b'Nothing lives here...', response.data)
      self.assertEqual(404, response.status_code)

if __name__ == "__main__":
  unittest.main()