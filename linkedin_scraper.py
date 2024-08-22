from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
import time
import getpass

class LinkedInScraper:
    def scrape(self):
        driver = webdriver.Chrome()
        events = self.login(driver)

        driver.quit()





    ###### Log in ##########
    def login(self,driver):
        driver.get('https://tr.linkedin.com/')

        driver.find_element(By.CLASS_NAME, 'nav__button-secondary').click()
        time.sleep(3)

        username = driver.find_element(By.ID, 'username')
        password = driver.find_element(By.ID, 'password')

        login_email = input("Your email:")
        username.send_keys(login_email)
        user_password=getpass.getpass()
        password.send_keys(user_password)

        sign_in_button = driver.find_element(By.CLASS_NAME, 'btn__primary--large')
        sign_in_button.click()
        print("Logged in successfully!")
        time.sleep(3)
        return self.events_page(driver)


    ###### Navigating Events Page ######
    def events_page(self,driver):
        driver.get('https://www.linkedin.com/events/')
        time.sleep(5)

        event_data = []
        while True:
            events = driver.find_elements(By.CLASS_NAME, 'events-events-card-container__card')
            try:
                if not events:
                    print("No events found.")
                for event in events:
                    try:
                        title = event.find_element(By.CSS_SELECTOR,'p.events-components-shared-discovery-card__event-title').text
                        date = event.find_element(By.CSS_SELECTOR, 'div.t-14.t-bold.mb1.mt2 span').text
                        location = 'Online'
                        link = event.find_element(By.CLASS_NAME, 'ember-view')
                        link = link.get_attribute('href')
                        event_data.append({
                            'Title': title,
                            'Date': date,
                            'Location': location,
                            'Link': link
                        })

                    except NoSuchElementException:
                        print("Could not find all elements in this event card.")
            except NoSuchElementException:
                print("Could not find all elements in this event card.")

            try:
                show_more_button = driver.find_element(By.XPATH, "//button[contains(@aria-label, 'Show More')]")
                show_more_button.click()
                time.sleep(3)

            except NoSuchElementException:
                break
        return event_data














