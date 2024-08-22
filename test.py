from eventbrite_scraper import EventbriteScraper
from conference_scraper import ConferenceIndexScraper
from linkedin_scraper import LinkedInScraper


def test_eventbrite_scraper(location, category):
    scraper = EventbriteScraper()
    all_events = scraper.scrape(location, category)

    for event in all_events:
        print(event)


def test_conference_scraper(location, category, user_month_choice):
    scraper = ConferenceIndexScraper()
    all_events = scraper.scrape(location, category, user_month_choice)

    for event in all_events:
        print(event)

def test_linkedin_scraper():
    scraper = LinkedInScraper()
    all_events = scraper.scrape()

    for event in all_events:
        print(event)


if __name__ == "__main__":
    test_conference_scraper(location='London', category='Business', user_month_choice='September 2024')
