import requests
from bs4 import BeautifulSoup




class EventbriteScraper:
    def get_page(self,url):
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        page = requests.get(url, headers=headers)

        if page.status_code == 200:

            soup = BeautifulSoup(page.text, 'html.parser')


            print(f"Page status: {page.status_code}")
            print(f"Page title: {soup.title.text}")

            return self.get_event_data(soup)

            if '404' in soup.title.text or 'Page Not Found' in soup.title.text:
                return False

        else:
            print(f"Failed to retrieve the webpage. Status code: {page.status_code}")
            return False


    def get_event_data(self,soup):
        events = soup.find_all('div', class_='SearchResultPanelContentEventCard-module__card___Xno0V')
        event_data=[]
        for event in events:
            # Extract event details
            title = event.find('h3',class_='Typography_root__487rx #3a3247 Typography_body-lg__487rx event-card__clamp-line--two Typography_align-match-parent__487rx')
            title= title.text if title else None


            date = event.find('p', class_='Typography_root__487rx #3a3247 Typography_body-md-bold__487rx Typography_align-match-parent__487rx')
            date = date.text if date else None

            location = event.find('p', class_='Typography_root__487rx #585163 Typography_body-md__487rx event-card__clamp-line--one Typography_align-match-parent__487rx')
            location = location.text if date else None

            link = event.find('a', class_='event-card-link')
            link = link['href'] if link else None

            #Append the event details to the list as a dictionary
            event_data.append({
                    'Title': title,
                    'Date': date,
                    'Location': location,
                    'Link': link
                    })
        return event_data

    def scrape(self, location, category):

        current_page = 1
        all_events = []
        while current_page<3:
            url = "https://www.eventbrite.com/d/" + str(location) + "/" + str(category) + "-events/?page=" + str(
                current_page) + ""
            print(f"Scraping page: {url}")
            event = self.get_page(url)
            if not event:
                print("no event found")
                break
            current_page += 1
            all_events.extend(event)

        return all_events

























