from selenium import webdriver
from bs4 import BeautifulSoup
import pprint
import time

class Event():
    """
    Event obj for calendar

    date
    location
    """

    def __init__(self, d, l):
        self.date = d
        self.location = l

class Calendar():
    """
    Calendar of UMD undergrad events

    events: list of events
    driver: webdriver
    """

    def __init__(self):
        self.events = set()

    def connect(self):
        # Connects to undergrad site
        base = "http://undergrad.cs.umd.edu/home"
        options = webdriver.ChromeOptions()
        options.add_argument('headless')
        driver = webdriver.Chrome(chrome_options=options)
        driver.get(base)
        event_links = set()

        for _ in range(12):
            time.sleep(1)
            soup = BeautifulSoup(driver.page_source, 'html.parser')
            
            for link in soup.find_all('a'):
                try:
                    if link['href'][:6] == '/event':
                        event_links.add(link['href'])
                except:
                    continue
                
            driver.find_element_by_class_name('icon-after').click()

        # parse events
        pprint.pprint(event_links)

c = Calendar()
c.connect()
