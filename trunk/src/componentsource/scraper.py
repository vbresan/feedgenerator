#!/usr/bin/python
# -*- coding: utf-8 -*-

################################################################################

import urllib
import logging

from componentsource.classes.CustomHTMLParser import CustomHTMLParser

################################################################################

def stripPage(page):
    
    beginIndex = page.find('<ul class="search">')
    if beginIndex != -1:
        
        endIndex = page.find('</ul>', beginIndex)
        if endIndex != -1:
            return page[beginIndex : endIndex]

    return ''

################################################################################

url = 'http://www.componentsource.com/newreleases/index.html' 

logging.info('Scraping URL: ' + url)

page = urllib.urlopen(url).read()
page = stripPage(page)

if len(page) != 0:
    
    htmlParser = CustomHTMLParser()
    htmlParser.feed(page)
    htmlParser.close()
        
logging.info('Done!')
