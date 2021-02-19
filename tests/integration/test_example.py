from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

options = Options()
options.add_argument('--headless')
driver = webdriver.Chrome(options=options)

# def find(self, by, value):
#     elements = self.driver.find_elements(by, value)
#     if len(elements) is 1:
#         return elements[0]
#     else:
#         return elements


driver.get('http://localhost:5000/')
element = driver.find_element(By.CSS_SELECTOR, '.display-4')
print(element.text)
driver.close()