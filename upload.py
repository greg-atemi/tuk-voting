import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time

# Read the Excel file
data = pd.read_excel('ELECTIONS.xlsx')

# Initialize the WebDriver (example uses Chrome)
driver = webdriver.Firefox()

# Open the target website (replace with your Django application's URL)
driver.get('http://localhost:8000/vote/admin_login')  # Change to your signup URL

actual_username = 'greg'
username_text_field = driver.find_element(By.NAME, 'username')
username_text_field.clear()
username_text_field.send_keys(actual_username)

actual_password = 'greg'
password_text_field = driver.find_element(By.NAME, 'pass1')
password_text_field.clear()
password_text_field.send_keys(actual_password)

login_button = driver.find_element(By.NAME, 'login')  # Change NAME based on your form

login_button.click()

# Open the target website (replace with your Django application's URL)
driver.get('http://localhost:8000/vote/create_election')  # Change to your signup URL

# Iterate through each row in the Excel file
for index, row in data.iterrows():
    election_name = row['Election Name']
    
    # Find the input fields and submit button
    election_name_field = driver.find_element(By.NAME, 'election_name')  # Change NAME based on your form
    submit_button = driver.find_element(By.NAME, 'submit2')  # Change NAME based on your form
    
    # Input the data
    election_name_field.clear()
    election_name_field.send_keys(election_name)
    
    # Click the signup button
    submit_button.click()
    
    # Add a delay to see the process (optional for debugging)
    # time.sleep(3)
    
    # Navigate back to the signup page for the next iteration
    driver.get('http://localhost:8000/vote/create_election')  # Change to your signup URL

# Close the browser
driver.quit()
