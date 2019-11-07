#!/usr/bin/env python3

"""This script was created to try scraping sms data (to look for spam)
   from 2 specific websites:
   https://receive-sms.com/ and https://freephonenum.com/us

   This script utilizes selenium 2 (selenium + webdriver = selenium2 lolwut).
   This script was designed with those 2 sites in mind, and will not be universal,
   so plz don't try just putting in a different site in the driver.get methods, as
   every site is designed differently."""

import csv
import time
from selenium import webdriver

#selenium webdriver object
#put in the absolute path for the geckodriver where the underlined portion is
DRIVER = webdriver.Firefox(executable_path=r"___________\geckoDRIVER.exe")


def web_scraper_receive_sms():
    """scraping method for the receivesms website that collects all of the source
       (of the spam) phone numbers, destination phone numbers, and message. It then
       puts a -1 at the end of the row because there wasn't a history of messages
       from the source phone number like there was from the freephonenum website"""

    with open("sms_spam_dataset.csv", 'a', encoding="utf-8") as csvfile:
        spamwriter = csv.writer(csvfile, delimiter=",")
        for num in range(0, 1000):
            DRIVER.get("https://receive-sms.com/?page={}".format(num))
            time.sleep(0.25)
            src_num = DRIVER.find_elements_by_xpath("//td[@data-title='[From]']")
            dst_num = DRIVER.find_elements_by_xpath("//td[@data-title='[To]']")
            msg = DRIVER.find_elements_by_xpath("//td[@data-title='[Message]']")

            src_num = [i.text.replace("[", "").replace("]", "").replace('X', '*')\
                      [1:] for i in src_num]
            print(src_num)
            dst_num = [i.text.replace("[", "").replace("]", "") for i in dst_num]
            msg = [i.text.replace("[", "").replace("]", "") for i in msg]
            add_page = zip(src_num, dst_num, msg)
            for entry in add_page:
                spamwriter.writerow([entry[0], entry[1], entry[2], -1])


def web_scraper_free_phone_num():
    """This method is used to scrape from the freephonenum website. It first grabs
       all the free phone numbers able to use without registration and then goes to
       each of the pages, scraping the source (of spam) phone number, destination
       phone number, message, as well as the hyperlink of the history of the messages
       from the source phone number (lol pretty cool of the website to do that for data
       collection)."""

    with open("sms_spam_dataset.csv", 'w', encoding="utf-8") as csvfile:
        spamwriter = csv.writer(csvfile, delimiter=",")
        spamwriter.writerow(["src_num", "dst_num", "msg", "url_for_history_for_number"])
        DRIVER.get("https://freephonenum.com/us/")
        nums = DRIVER.find_elements_by_xpath\
               ("//a[@class='numbers-btn btn btn-secondary btn-block ']")
        nums = [i.text[1:17].replace(') ', '').replace('-', '')\
               .replace(' (', '') for i in nums]
        for phone_number in nums:
            print(phone_number)
            DRIVER.get("https://freephonenum.com/us/receive-sms/{}".format(phone_number[1::]))
            time.sleep(0.1)
            #text info
            scraped_info = DRIVER.find_elements_by_xpath("//td")
            src_num = [i.text.replace('-', "") for i in scraped_info if i.text != ""][4::3]
            msg = [i.text for i in scraped_info if i.text != ""][5::3]
            dst_num = phone_number[1::]

            #urls
            scraped_url = DRIVER.find_elements_by_xpath("//a[@href]")
            url_for_history_for_number = [i.get_attribute("href") for i in scraped_url \
                                         if "receive-sms-from" in i.get_attribute("href")]
            url_for_history_for_number = url_for_history_for_number\
                                         [1:len(url_for_history_for_number)-11]
            add_page = zip(src_num, msg, url_for_history_for_number)
            for entry in add_page:
                spamwriter.writerow([entry[0], dst_num, entry[1], entry[2]])

web_scraper_free_phone_num()
web_scraper_receive_sms()
