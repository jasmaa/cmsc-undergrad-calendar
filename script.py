from selenium import webdriver
from bs4 import BeautifulSoup
import pprint
import time

class Event():
    """
    Event obj for calendar

    title
    start_date
    end_date
    location
    """

    def __init__(self, d, l):
        self.date = d
        self.location = l

class Calendar():
    """
    Calendar of UMD undergrad events

    events: list of events
    """

    def __init__(self):
        self.events = set()

    def connect(self):
        
        # Connects to undergrad site
        base = "http://undergrad.cs.umd.edu"
        options = webdriver.ChromeOptions()
        options.add_argument('headless')
        driver = webdriver.Chrome(chrome_options=options)
        driver.get(base+"/home")
        
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
        for link in event_links:
            driver.get(base+link)
            s = BeautifulSoup(driver.page_source, 'html.parser')

            raw_title = s.title
            raw_single = s.find("span", class_="date-display-single")
            raw_start = s.find("span", class_="date-display-start")
            raw_end = s.find("span", class_="date-display-end")

            print(raw_title.getText()[0:raw_title.getText().find(" | ")])
            if raw_single != None:
                print(raw_single.getText())
            if raw_start != None:
                print(raw_start.getText())
            if raw_end != None:
                print(raw_end.getText())
            print()
        

c = Calendar()
c.connect()

                  
