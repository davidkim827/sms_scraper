# sms_scraper

This script was created to collect data on sms messages to hopefully capture some spam data. The script was designed with 4 specific websites in mind:

1. https://receive-sms.com/
2. https://freephonenum.com/us
3. https://fakenum.com/receive-free-sms-online?country=United%20States, 
4. https://getfreesmsnumber.com/free-receive-sms-from-us


The script has been hardcoded for those specific websites and for the number of pages to iterate through (at least for the first website of the first 2000 pages). This creates roughly around 66,000 datapoints and the script returns a csv file with all those datapoints. Interesting thing to note is that the second website (freephonenum) gives you a link to the history of messages from the source phone number (of the possible spam or ham or w.e.). I have therefore placed the URL as the last element of the datapoints where it exists. The first website (receivesms) doesn't have that, and therefore as any good data scientist would (lul i'm not a DS by any means) I put in a -1!!!! So proud (: Enjoy the script!

Also have placed what I have collected for 11/2019

Further improvements for future:
multithreading for IO
etc.

P.S. plz don't yell at me for my PEP8 formatting... black did it all for me lul

Dataset explanation:

src_num = source phone number (of the potential spam or whoever sent the text message)
dst_num = phone number sourced from the websites
msg = message
url_for_history_for_number = links from freephonenum.com
