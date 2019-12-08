#!/usr/bin/env python3

"""This script was created to try scraping sms data (to look for spam)
   from 4 specific websites:
   [https://receive-sms.com/, 
    https://freephonenum.com/us, 
    https://fakenum.com/receive-free-sms-online?country=United%20States, 
    https://getfreesmsnumber.com/free-receive-sms-from-us]

   This script utilizes selenium 2 (selenium + webdriver = selenium2 lolwut).
   This script was designed with those 4 sites in mind, and will not be universal,
   so plz don't try just putting in a different site in the driver.get methods, as
   every site is designed differently."""

import csv
import time
import os
import sys
from selenium import webdriver

# selenium webdriver object
# put in the absolute path for the geckodriver where the underlined portion is
DRIVER = webdriver.Firefox(executable_path=r"_________\geckoDRIVER.exe")
EXISTING_DATAPOINTS = set()


def load_set_with_former_datapoints():
    """Loads all datapoints into a set to be able to not duplicate datapoints"""
    with open("sms_spam_dataset.csv", "r", encoding="utf-8") as csvfile:
        spamreader = csv.reader(csvfile, delimiter=",")
        for row in spamreader:
            if not row:
                continue
            EXISTING_DATAPOINTS.add(tuple(row))
    csvfile.close()


def web_scraper_fakenum():
    """scraping method for the fakenum website that collects all of the source
    (of the spam) phone numbers, destination phone numbers, and message. It then
    puts a -1 at the end of the row because there wasn't a history of messages
    from the source phone number like there was from the freephonenum website"""

    DRIVER.get("https://fakenum.com/receive-free-sms-online?country=United%20States")
    with open("sms_spam_dataset.csv", "a", encoding="utf-8") as csvfile:
        spamwriter = csv.writer(csvfile, delimiter=",")
        nums_links = DRIVER.find_elements_by_xpath("//a[@class='btn btn-info btn-sm']")
        nums_links = [i.get_attribute("href") for i in nums_links]
        numbers = [i[-10:] for i in nums_links]
        for num in range(len(nums_links)):
            DRIVER.get(nums_links[num])
            dst_num = numbers[num]
            print(dst_num)
            info = DRIVER.find_elements_by_xpath("//td")
            src_nums = [i.text for i in info][3::3]
            msgs = [i.text for i in info][5::3]
            for i in range(len(src_nums)):
                src_num = src_nums[i]
                msg = msgs[i]
                row_to_write = (src_num, dst_num, msg, -1)
                if row_to_write in EXISTING_DATAPOINTS:
                    continue
                spamwriter.writerow(list(row_to_write))
                print("{}\n{}\n".format(src_num, msg))


def web_scraper_getfreesmsnumber():
    """scraping method for the getfreesmsnumber website that collects all of the source
    (of the spam) phone numbers, destination phone numbers, and message. It then
    puts a -1 at the end of the row because there wasn't a history of messages
    from the source phone number like there was from the freephonenum website"""

    DRIVER.get("https://getfreesmsnumber.com/login/login.php")
    username = DRIVER.find_element_by_name("username")
    password = DRIVER.find_element_by_name("password")

    # fills out the username and password forms and "clicks" the link with a throwaway account. you're welcome.
    username.send_keys("throwaway123")
    password.send_keys("throwaway123!@#")
    DRIVER.find_element_by_id("btn-login").click()
    time.sleep(1)
    DRIVER.get("https://getfreesmsnumber.com/free-receive-sms-from-us")

    with open("sms_spam_dataset.csv", "a", encoding="utf-8") as csvfile:
        spamwriter = csv.writer(csvfile, delimiter=",")
        nums_links = DRIVER.find_elements_by_xpath("//a[@class='clickcheck']")
        nums_links = [i.get_attribute("href") for i in nums_links]
        numbers = [i[-10:] for i in nums_links]
        print(numbers)
        for num in range(len(nums_links)):
            DRIVER.get(nums_links[num])
            dst_num = numbers[num]
            print(dst_num)
            while 1:
                try:
                    content = DRIVER.find_elements_by_xpath(
                        "//div[@class='contentresult']"
                    )
                    all_text = [
                        i.text.split("\n") for i in content if "Voicemail" not in i.text
                    ]
                    for text in all_text:
                        src_num = text[0][-10:]
                        msg = text[1]
                        row_to_write = (src_num, dst_num, msg, -1)
                        if row_to_write in EXISTING_DATAPOINTS:
                            continue
                        spamwriter.writerow(list(row_to_write))
                        print("{}\n{}\n".format(src_num, msg))
                    DRIVER.find_element_by_xpath(
                        "//a[text()[contains(.,'Next')]]"
                    ).click()
                except Exception as e:
                    print(e)
                    break
    csvfile.close()


def web_scraper_receivesms():
    """scraping method for the receivesms website that collects all of the source
       (of the spam) phone numbers, destination phone numbers, and message. It then
       puts a -1 at the end of the row because there wasn't a history of messages
       from the source phone number like there was from the freephonenum website"""

    with open("sms_spam_dataset.csv", "a", encoding="utf-8") as csvfile:
        spamwriter = csv.writer(csvfile, delimiter=",")
        for num in range(0, 2000):
            DRIVER.get("https://receive-sms.com/?page={}".format(num))
            time.sleep(0.25)
            src_num = DRIVER.find_elements_by_xpath("//td[@data-title='[From]']")
            dst_num = DRIVER.find_elements_by_xpath("//td[@data-title='[To]']")
            msg = DRIVER.find_elements_by_xpath("//td[@data-title='[Message]']")

            src_num = [
                i.text.replace("[", "").replace("]", "").replace("X", "*")[1:]
                for i in src_num
            ]
            dst_num = [i.text.replace("[", "").replace("]", "") for i in dst_num]
            msg = [i.text.replace("[", "").replace("]", "") for i in msg]
            add_page = zip(src_num, dst_num, msg)
            for entry in add_page:
                print(entry[0])
                print(entry[1])
                print(entry[2])
                row_to_write = (entry[0], entry[1], entry[2], -1)
                if row_to_write in EXISTING_DATAPOINTS:
                    csvfile.close()
                    return
                spamwriter.writerow(list(row_to_write))
    csvfile.close()


def web_scraper_freephonenum():
    """This method is used to scrape from the freephonenum website. It first grabs
       all the free phone numbers able to use without registration and then goes to
       each of the pages, scraping the source (of spam) phone number, destination
       phone number, message, as well as the hyperlink of the history of the messages
       from the source phone number (lol pretty cool of the website to do that for data
       collection)."""
    with open("sms_spam_dataset.csv", "a", encoding="utf-8") as csvfile:
        spamwriter = csv.writer(csvfile, delimiter=",")
        header = ("src_num", "dst_num", "msg", "url_for_history_for_number")
        if header not in EXISTING_DATAPOINTS:
            spamwriter.writerow(list(header))
        DRIVER.get("https://freephonenum.com/us/")

        # gives time to utilize single sign on via fb/google
        time.sleep(35)

        # goes back and starts scraping
        DRIVER.get("https://freephonenum.com/us/")
        nums = DRIVER.find_elements_by_xpath(
            "//a[@class='numbers-btn btn btn-secondary btn-block ']"
        )
        nums = [
            i.text[1:17].replace(") ", "").replace("-", "").replace(" (", "")
            for i in nums
        ]
        for phone_number in nums:
            print(phone_number)
            DRIVER.get(
                "https://freephonenum.com/us/receive-sms/{}".format(phone_number[1::])
            )

            time.sleep(0.1)

            # text info
            scraped_info = DRIVER.find_elements_by_xpath("//td")
            src_num = [i.text.replace("-", "") for i in scraped_info if i.text != ""][
                4::3
            ]
            msg = [i.text for i in scraped_info if i.text != ""][5::3]
            dst_num = phone_number[1::]

            # urls
            scraped_url = DRIVER.find_elements_by_xpath("//a[@href]")
            url_for_history_for_number = [
                i.get_attribute("href")
                for i in scraped_url
                if "receive-sms-from" in i.get_attribute("href")
            ]
            url_for_history_for_number = url_for_history_for_number[
                1 : len(url_for_history_for_number) - 11
            ]
            add_page = zip(src_num, msg, url_for_history_for_number)
            for entry in add_page:
                row_to_write = (entry[0], dst_num, entry[1], entry[2])
                if row_to_write in EXISTING_DATAPOINTS:
                    continue
                spamwriter.writerow(list(row_to_write))
    csvfile.close()


load_set_with_former_datapoints()
web_scraper_freephonenum()
web_scraper_receivesms()
web_scraper_getfreesmsnumber()
web_scraper_fakenum()
