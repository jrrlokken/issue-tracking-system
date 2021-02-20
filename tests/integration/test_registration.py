import unittest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

options = Options()
options.add_argument('--headless')

class ITSRegistration(unittest.TestCase):
  def setUp(self):
    self.driver = webdriver.Chrome(options=options)

  def tearDown(self):
    self.driver.close()

  def test_register_with_ITS(self):
    """Get the homepage, click Register, register a new account."""
    driver = self.driver
    driver.get('https://its.joshualokken.tech')
    self.assertIn('Issue Tracking System', driver.title)

    register = driver.find_element(By.ID, 'register')
    register.click()
    lead = driver.find_element(By.CSS_SELECTOR, '.lead')
    assert 'Register for an account' in lead.text

    # Get the fields and button
    email = driver.find_element(By.ID, 'email')
    fname = driver.find_element(By.ID, 'first_name')
    lname = driver.find_element(By.ID, 'last_name')
    password = driver.find_element(By.ID, 'password')
    confirm = driver.find_element(By.ID, 'confirm')
    button = driver.find_element(By.ID, 'register-submit')

    # Fill in fields and submit
    email.send_keys('george@example.com')
    fname.send_keys('George')
    lname.send_keys('Jefferson')
    password.send_keys('password')
    confirm.send_keys('password')
    button.click()

    # Make sure we get the welcome text
    heading = driver.find_element(By.TAG_NAME, 'h1')
    assert 'Welcome' in heading.text

if __name__ == "__main__":
  unittest.main()

