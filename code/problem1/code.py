import time, csv, re
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import json

# driver_path = '/Applications/chromedriver-mac-x64'  
brave_path = '/Applications/Brave Browser'

options = Options()
options.binary_location = brave_path

# Create a WebDriver instance with the specified options
service = Service()
driver = webdriver.Chrome(service=service, options=options)

driver.get('https://www.indiegogo.com/explore/home?project_timing=all&product_stage=all&sort=trending')
driver.implicitly_wait(10)

button_class_name = 'button-class-name'  # Replace with the actual class name of the button
button = driver.find_element(By.CLASS_NAME, 'projectDiscoverableCard-imageOverlay')

# Click the button
button.click()
time.sleep(5)


# wanted fields classes
creatorClass = 'campaignOwnerName-tooltip'
titleClass = 'basicsSection-title desktop'
textClass = 'basicsSection-tagline desktop'
dollarPledgedClass ='basicsGoalProgress-amountSold'
numBackersClass = 'basicsGoalProgress-claimedOrBackers'
daysToGoClass = 'basicsGoalProgress-progressDetails-detailsTimeLeft'
flexibleGoalClass = 'basicsGoalProgress-progressDetails-detailsGoal-goalPercentageOrInitiallyRaised'
dollarGoalClass = 'basicsGoalProgress-progressDetails-detailsGoal-goalPercentageOrInitiallyRaised'


flexible = driver.find_element(By.CLASS_NAME, 'basicsGoalProgress-progressDetails-detailsGoal-goalWording')
if flexible:
    flexibleGoal = driver.find_element(By.CLASS_NAME, flexibleGoalClass).text
    flexibleGoal = re.search(r'\d+%', flexibleGoal)
    flexibleGoal = flexibleGoal.group()
    dollarGoal = None
else:
    dollarGoal = driver.find_element(By.CLASS_NAME, dollarGoalClass).text
    dollarGoal = re.sub(r'[^\d.]', '', dollarGoal)
    flexibleGoal = None

creator = driver.find_element(By.CLASS_NAME, creatorClass)
title = driver.find_element(By.CLASS_NAME, titleClass)

text = driver.find_element(By.CLASS_NAME, textClass)
dollarPledged = driver.find_element(By.CLASS_NAME, dollarPledgedClass)
numBackers = driver.find_element(By.CLASS_NAME, numBackersClass)
daysToGo = driver.find_element(By.CLASS_NAME, daysToGoClass)

creator = creator.text
title = title.text
text = text.text
dollarPledged = dollarPledged.text
numBackers = numBackers.text
daysToGo = daysToGo.text

# dollarPledged = driver.find_element(By.CLASS_NAME, dollarPledgedClass).text
dollarPledged = re.sub(r'[^\d.]', '', dollarPledged)
numBackers = re.sub(r'[^\d.]', '', numBackers)
daysToGo = re.sub(r'[^\d.]', '', daysToGo)
"""
try:
    dollars_goal = driver.find('div', class_='discoverableCard-goal').text.strip()
    dollars_goal = re.sub(r'[^\d.]', '', dollars_goal)
except AttributeError:
    dollars_goal = None

try:
    num_backers = driver.find('div', class_='discoverableCard-backers').text.strip()
    num_backers = re.sub(r'[^\d.]', '', num_backers)
except AttributeError:
    num_backers = None

try:
    days_to_go = driver.find('div', class_='discoverableCard-timeLeft').text.strip()
    days_to_go = re.sub(r'[^\d.]', '', days_to_go)
except AttributeError:
    days_to_go = None
"""
driver.quit()

# Store the data in a dictionary
data = {
    'creator': creator,
    'title': title,
    'text': text,
    'dollarPledged': dollarPledged,
    'numBackers': numBackers,
    'daysToGo': daysToGo,
    'flexibleGoal': flexibleGoal,
    'dollarGoal': dollarGoal
}

# Save the dictionary to a JSON file
with open('data.json', 'w') as json_file:
    json.dump(data, json_file, indent=4)
# the_soup = BeautifulSoup(driver.page_source, 'html.parser')

