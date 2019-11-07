# sms_scraper

This script was created to collect data on sms messages to hopefully capture some spam data. The script was designed with 2 specific websites in mind:

1. https://receive-sms.com/
2. https://freephonenum.com/us

The script has been hardcoded for those specific websites and for the number of pages to iterate through (at least for the first website of the first 1000 pages). This creates roughly around 16,000 datapoints and the script returns a csv file with all those datapoints. Interesting thing to note is that the second website (freephonenum) gives you a link to the history of messages from the source phone number (of the possible spam or ham or w.e.). I have therefore placed the URL as the last element of the datapoints where it exists. The first website (receivesms) doesn't have that, and therefore as any good data scientist would (lul i'm not a DS by any means) I put in a -1!!!! So proud (: Enjoy the script!

Further improvements for future:
multithreading for IO
etc.

P.S. plz don't yell at me for my PEP8 formatting... pylint is very strict lul
