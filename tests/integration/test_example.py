from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

# options = Options()
# options.add_argument('--headless')
# driver = webdriver.Chrome(options=options)

driver = webdriver.Chrome()

# driver.get('http://localhost:5000/')
# element = driver.find_element(By.CSS_SELECTOR, '.display-4')
# print(element.text)
# driver.close()

driver.get('http://localhost:5000/login')
email = driver.find_element(By.ID, 'email')
password = driver.find_element(By.ID, 'password')
form = driver.find_element(By.ID, 'login-form')
button = driver.find_element(By.CSS_SELECTOR, '#login-button')
email.send_keys('testuser2@example.com')
password.send_keys('password')
button.click()