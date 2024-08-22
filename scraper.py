from conference_scraper import ConferenceIndexScraper
from linkedin_scraper import LinkedInScraper
from eventbrite_scraper import EventbriteScraper
import csv


class Scraper:
    def __init__(self):
        self.linkedin_scraper =LinkedInScraper()
        self.eventbrite_scraper = EventbriteScraper()
        self.conference_index_scraper = ConferenceIndexScraper()

    def run(self):
        # Implement logic to run all scrapers

        location = input("Enter a Location:").replace(' ', '--')  # Avoid spaces
        category = input("Category:")
        user_month_choice = input("Select a month and year for conferences (e.g., 'August, 2024'): ").strip()

        all_events = []
        print("Running LinkedIn Scraper...")
        linkedin_events = self.linkedin_scraper.scrape()  # All events şn events suggestion page

        if linkedin_events:
            filtered_linkedin_events = self.filter_event(linkedin_events, category)  # Filtered based on category
            print("Linkedin Events:")
            self.print_event(filtered_linkedin_events)
            all_events.extend(filtered_linkedin_events)
        else:
            print(f"No events for {category} in Linkedn Events page.")

        print("Running Eventbrite Scraper...")
        eventbrite_events = self.eventbrite_scraper.scrape(location, category)
        print("Eventbrite Events:")
        self.print_event(eventbrite_events)
        all_events.extend(eventbrite_events)

        print("Running Conference Index Scraper...")
        conference_index_events = self.conference_index_scraper.scrape(location, category, user_month_choice)
        print("Conferences:")
        self.print_event(conference_index_events)
        all_events.extend(conference_index_events)

        self.saving_data(all_events, location, category)

    def print_event(self, event_data):
        for event in event_data:
            print(f"Title: {event['Title']}\nDate: {event['Date']}\nLink:{event['Link']}\n")


    def filter_event(self, event_data, category):
        filtered_events = []
        for event in event_data:
            if category.lower() in event['Title'].lower():
                filtered_events.append(event)
        return filtered_events


    def saving_data(self, all_events, location, category):
        markdown_file = f"{category}_events_{location}.md"
        with open(markdown_file, 'w', encoding='utf-8') as file:
            file.write("| Title | Date | Location | Link |\n")
            file.write("|-------|------|----------|------|\n")
            for event in all_events:
                file.write(
                    f"| {event['Title']} | {event['Date']} | {event['Location']} | [Link]({event['Link']}) |\n")
        print(f"Markdown data saved to {markdown_file}")


if __name__ == "__main__":
    scraper = Scraper()
    scraper.run()
