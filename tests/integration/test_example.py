from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

# options = Options()
# options.add_argument('--headless')
# driver = webdriver.Chrome(options=options)

# def find(self, by, value):
#     elements = self.driver.find_elements(by, value)
#     if len(elements) is 1:
#         return elements[0]
#     else:
#         return elements
driver = webdriver.Chrome()

driver.get('http://localhost:5000/')
element = driver.find_element(By.CSS_SELECTOR, '.display-4')
print(element.text)
driver.close()

driver.get('https://flask-its.herokuapp.com/login')
email = driver.find_element(By.ID, 'email')
password = driver.find_element(By.ID, 'password')
email.send_keys('testuser@example.com')
password.send_keys('password')