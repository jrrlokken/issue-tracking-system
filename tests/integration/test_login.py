import unittest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

options = Options()
options.add_argument('--headless')

class ITSLoginCreation(unittest.TestCase):
  def setUp(self):
    self.driver = webdriver.Chrome(options=options)

  def tearDown(self):
    self.driver.close()

  def test_login_and_create_issue(self):
    # Get the login page and login
    driver = self.driver
    driver.get('https://its.joshualokken.tech/login')
    email = driver.find_element(By.ID, 'email')
    password = driver.find_element(By.ID, 'password')
    button = driver.find_element(By.CSS_SELECTOR, '#login-button')
    email.send_keys('george@example.com')
    password.send_keys('password')
    button.click()

    # Wait 5 seconds, then click the New Issue navigation link
    driver.implicitly_wait(5)
    newItemNav = driver.find_element(By.ID, 'new-issue')
    newItemNav.click()

    # Wait 5 seconds, then create and submit a new issue
    driver.implicitly_wait(5)
    title = driver.find_element(By.ID, 'title')
    text = driver.find_element(By.ID, 'text')
    submit = driver.find_element(By.ID, 'new-issue-submit')
    title.send_keys('**TEST ISSUE**')
    text.send_keys('Test issue description')
    submit.click()

  def tearDown(self):
    self.driver.close()

if __name__ == "__main__":
  unittest.main()