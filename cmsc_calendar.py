from selenium import webdriver
from bs4 import BeautifulSoup
import pprint
import time
import dateparser

class Event():
    """
    Event obj for calendar

    title : title
    content : post content
    start_time : start unix time
    end_time : end unix time
    """

    def __init__(self, t, c, st, et):
        self.title = t
        self.content = c
        self.start_time = st
        self.end_time = et

    def __str__(self):
        return self.title + ": " + self.content

    def get_start(self):
        return "T".join(str(self.start_time).split(" "))
    def get_end(self):
        return "T".join(str(self.end_time).split(" "))

class Calendar():
    """
    Calendar of UMD undergrad events

    events: list of events
    """

    def __init__(self):
        self.events = []

    def connect(self):
        # connects to umd cs undergrad site
        base = "http://undergrad.cs.umd.edu"
        options = webdriver.ChromeOptions()
        options.add_argument('headless')
        driver = webdriver.Chrome(chrome_options=options)
        driver.get(base+"/home")

        event_links = self.get_event_links(driver, base)
        self.parse_events(driver, base, event_links)

        #webdriver.quit()

    def get_event_links(self, driver, base):
        # gets list of event links
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

        return event_links
        
    def parse_events(self, driver, base, event_links):
        # parses events into calendar
        for link in event_links:
            driver.get(base+link)
            s = BeautifulSoup(driver.page_source, 'html.parser')

            raw_title = s.title
            raw_content = s.find("div", class_="field-item even")
            raw_single = s.find("span", class_="date-display-single")
            raw_start = s.find("span", class_="date-display-start")
            raw_end = s.find("span", class_="date-display-end")

            title = raw_title.getText()[0:raw_title.getText().find(" | ")].strip()
            content= raw_content.getText()

            # parse time
            if raw_single != None:
                raw_single = raw_single.getText()
            if raw_start != None:
                raw_start = raw_start.getText()
            if raw_end != None:
                raw_end = raw_end.getText()
                
            start_time, end_time = Calendar.parse_time(raw_single, raw_start, raw_end)
            
            event = Event(title, content, start_time, end_time)
            self.events.append(event)
            
    @staticmethod
    def parse_time(single, start, end):
        # all day, range
        if single == None:
            start_time = start[:start.find("(")-1]
            end_time = end[:end.find("(")-1] + " 23:59"
        # all day, single day
        elif start == None and end == None:
            start_time = single[:single.find("(")-1]
            end_time = single[:single.find("(")-1] + " 23:59"
        # time
        else:
            date = single[:single.find(" - ")]
            start_time = date + " " + start
            end_time = date + " " + end

        return dateparser.parse(start_time), dateparser.parse(end_time)
