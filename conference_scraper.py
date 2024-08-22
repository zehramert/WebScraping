from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
import time

class ConferenceIndexScraper:
    def scrape(self, location, category, user_month_choice):
        driver = webdriver.Chrome()

        driver.get('https://conferenceindex.org/')
        time.sleep(2)

        events = self.city_detection(driver, location, category, user_month_choice)


        driver.quit()
        return events  # Return the events list for further use

    def city_detection(self, driver, location, category, user_month_choice):
        try:
            # Find all city links on the page
            city_links = driver.find_elements(By.CSS_SELECTOR, 'a.list-group-item.list-group-item-action')

            for city in city_links:
                if location.lower() in city.get_attribute('title').lower():
                    city.click()
                    time.sleep(3)
                    print(f"Navigated to conferences in {location}")
                    return self.discipline_detection(driver,category, user_month_choice)

            print(f"No conferences found for {location}.")
            return None  # Return None if no city is found

        except NoSuchElementException:
            print(f"Could not find a city or discipline link.")
            return None  # Return None in case of an exception

    def discipline_detection(self, driver, category, user_month_choice):
        # If city was found, proceed to discipline selection

        try:
            discipline_links = driver.find_elements(By.CSS_SELECTOR, 'a[title]')

            for discipline in discipline_links:
                if category.lower() in discipline.get_attribute('title').lower():
                    discipline.click()
                    time.sleep(3)
                    print(f"Navigated to conferences for {category}")
                    return self.month_detection(driver, user_month_choice)

            print(f"No conferences found for {category}.")
            return None  # Return None if no discipline is found

        except NoSuchElementException:
            print("Error while selecting discipline.")
            return None  # Return None in case of an exception

    def month_detection(self, driver, user_month_choice):
        conference_blocks = driver.find_elements(By.CLASS_NAME, 'card-year')



        ##### Splitted the user input to fit it into right format ###
        parts = user_month_choice.split()

        month_part=parts[0]
        year_part=parts[1]

        user_month_choice = f'{month_part}, {year_part}'

        for block in conference_blocks:
            month_year = block.find_element(By.CLASS_NAME, 'card-header').text
            if user_month_choice.lower() in month_year.lower():
                try:
                    conference_items = block.find_elements(By.CSS_SELECTOR, 'li')
                    return self.return_event_data(conference_items)
                except NoSuchElementException:
                    print("Could not find all elements in this conference entry.")
                    continue

        print(f"No conferences found for {user_month_choice}.")
        return []

    def return_event_data(self, conference_items):
        events = []
        for item in conference_items:
            date = item.text.split()[0:2]  # Extracting the date
            title_element = item.find_element(By.TAG_NAME, 'a')
            title = title_element.get_attribute('title')
            link = title_element.get_attribute('href')
            location = item.text.split('-')[-1].strip()  # Extracting the location after the hyphen

            events.append({
                "Date": ' '.join(date),
                "Title": title,
                "Location": location,
                "Link": link
            })

        return events
