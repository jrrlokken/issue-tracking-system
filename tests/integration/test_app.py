import unittest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

# options = Options()
# options.add_argument('--headless')
# driver = webdriver.Chrome(options=options)
class ITSRegister(unittest.TestCase):
  def setUp(self):
    self.driver = webdriver.Chrome()

  def test_register_with_ITS(self):
    """Get the homepage, click Register, register a new account."""
    driver = self.driver
    driver.get('https://its.joshualokken.tech')
    self.assertIn('Issue Tracking System', driver.title)

    register = driver.find_element(By.ID, 'register')
    register.click()
    lead = driver.find_element(By.CSS_SELECTOR, '.lead')
    assert 'Register for an account' in lead.text

  def tearDown(self):
    self.driver.close()

if __name__ == "__main__":
  unittest.main()

# Get the fields and button
# email = driver.find_element(By.ID, 'email')
# fname = driver.find_element(By.ID, 'first_name')
# lname = driver.find_element(By.ID, 'last_name')
# password = driver.find_element(By.ID, 'password')
# confirm = driver.find_element(By.ID, 'confirm')
# button = driver.find_element(By.ID, 'register-submit')

# # Fill in fields and submit
# email.send_keys('george@example.com')
# fname.send_keys('George')
# lname.send_keys('Jefferson')
# password.send_keys('password')
# confirm.send_keys('password')
# button.click()
# driver.implicitly_wait(5)

# # Make sure we get the welcome text
# heading = driver.find_element(By.CSS_SELECTOR, '.display-4')
# assert 'Welcome to ITS' in heading.text

# # Get the login page and login
# driver.get('https://its.joshualokken.tech/login')
# email = driver.find_element(By.ID, 'email')
# password = driver.find_element(By.ID, 'password')
# button = driver.find_element(By.CSS_SELECTOR, '#login-button')
# email.send_keys('user1@example.com')
# password.send_keys('password1')
# button.click()

# # Wait 5 seconds, then click the New Issue navigation link
# driver.implicitly_wait(5)
# newItemNav = driver.find_element(By.ID, 'new-issue')
# newItemNav.click()

# # Wait 5 seconds, then create and submit a new issue
# driver.implicitly_wait(5)
# title = driver.find_element(By.ID, 'title')
# text = driver.find_element(By.ID, 'text')
# submit = driver.find_element(By.ID, 'new-issue-submit')
# title.send_keys('**TEST ISSUE**')
# text.send_keys('Test issue description')
# submit.click()

# driver.close()

