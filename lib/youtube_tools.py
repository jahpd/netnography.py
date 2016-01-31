from urllib2 import urlopen
from bs4 import *
import re
import datetime
from iso88591 import *

def yt(query, fn):
    try:
        print "=> Searching for results ..."
        
        # PROCESS QUERY TO GENERATE PROPER LINK
        url = "https://www.youtube.com/results?search_query=%s" % "+".join([p for p in query.split(" ")])
        extract(soup_url(url), fn)
    except IOError as e:
        print e.strerror

def soup_url(url):   
    print "=> %s: requesting %s " % (datetime.datetime.now(), url)
    html = urlopen(url).read()
    return  BeautifulSoup(html, "lxml")

def soup_string(html):
    return BeautifulSoup(html, "lxml")

def extract(soup, fn):
    items = soup.find('ol', id=re.compile(r'item-section-[0-9]*'))
    dd = {}
    for item in items.find_all('li'):
        # titulo
        t = item.find('a', title=re.compile(r'\w*'), href=re.compile(r'\/watch\?v=[a-zA-Z0-9?\S]+'))
        if t != None:
            dd = {"url": "https://www.youtube.com%s" % t["href"], "description": {"info":"", "text":""}, "title": t["title"]}
        # metainfo
            _bs = soup_url(dd["url"])
            dd["description"]["info"] = _bs.find('div', id="watch-uploader-info").text
            dd["description"]["text"] = _bs.find('p', id="eow-description").text
            fn(dd)

    nextlink= "https://www.youtube.com%s" % soup.find('div', class_="yt-uix-pager search-pager branded-page-box spf-link ").find('a', {"data-link-type": "next", "href": re.compile(r'\/results\?search_query=[a-zA-Z0-9]+(\+[a-zA-Z0-9]+)*\&page=[0-9]+')})['href']
    
    if not "/user/" in nextlink:
        extract(soup_url(nextlink), fn)


from datetime import datetime

def markdown(data, fn):
    cursor = fn()
    s = "|  " + "  |  ".join([p for p in cursor[0]]) + " |\n|"
    s = s + ":|".join([("-"*6) for p in cursor[0]]) + "|\n|"
    for videos in cursor:
        for video in videos:
            if video == "url":
                s = ("%s [video](%s) |") % (s, videos[video])
    
            if video ==  "_id":
                s = ("%s %s |") % (s, videos[video])
                
            if video == "description":
                for k in videos[video]:
                    s = (("%s %s |") % (s, videos[video][k])) or "None"
        s = s + "\n|"
    return s


def write(name, data):
    print "writing data/%s.json" % name
    f = open("../data/%s.json" % name, "w+")
    f.write(json.dumps(data))  #f.write(json.dumps(data))
    f.close()
