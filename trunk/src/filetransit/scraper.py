#!/usr/bin/python
# -*- coding: utf-8 -*-

################################################################################

import urllib
import logging

from filetransit.classes.CustomHTMLParser import CustomHTMLParser

################################################################################

def stripPage(page):
    
    beginIndex = page.find('<div id="content">')
    if beginIndex != -1:
        
        endIndex = page.find('<div id="siteInfo">', beginIndex)
        if endIndex != -1:
            return page[beginIndex : endIndex]

    return ''

################################################################################

url = 'http://www.filetransit.com/index.php?action=new' 

logging.info('Scraping URL: ' + url)

page = urllib.urlopen(url).read()
page = stripPage(page)

if len(page) != 0:
    
    htmlParser = CustomHTMLParser()
    htmlParser.feed(page)
    htmlParser.close()
        
logging.info('Done!')
