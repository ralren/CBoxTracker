'''
Created on August 6, 2013
@summary: This script follows the RSS feed of a given CBOX and alerts user if there's a new message. The code for checkRSS() 
originated and was modified from Whats_Calculus' comment in this Reddit thread: 
http://www.reddit.com/r/raspberry_pi/comments/19pr93/using_my_raspberry_pi_to_monitor_an_rss_feed/
@author: Ren
'''

import win32ui, win32con, feedparser, time, requests, urllib2, bs4

'''
@summary: This function takes the RSS feed URL and parses through it. It takes the most recent message from the feed and checks if
this is altered. If so, it displays the new message and asks if the user wishes to continue monitoring the feed.
'''
def checkRSS(cbox):
    r = requests.head(cbox)
    c = feedparser.parse(cbox)
    message = c.entries[0].description
    answer = True
    while answer:
        if r.status_code == 304:
            time.sleep(30)
        elif r.status_code == 200:
            r1 = requests.get(cbox)
            d = feedparser.parse(r1.content)
            newMessage = d.entries[0].description
            if message != newMessage:
                win32ui.MessageBox(newMessage, 'CBox Alert!', win32con.MB_OK)
                if win32ui.MessageBox('Would you like to continue monitoring the CBox?', 'CBox Monitoring', win32con.MB_YESNO) == win32con.IDNO:
                    answer = False
                message = newMessage
        else:
            time.sleep(30)
            
'''
@summary: This function takes a given URL and extracts the RSS feed URL from it.
@return: extract the RSS feed URL
'''
def extractRSS(url):
    opening = urllib2.urlopen(url)
    html = opening.read()
    soup = bs4.BeautifulSoup(html)
    extract = soup.link.get('href')
    return extract

'''
@summary: Starts the program and asks for the quick link of the CBox to be monitored.
'''
def main():
    url = raw_input("Please type your CBox's quick link: ")
    checkRSS(extractRSS(url))
main()
