#!/usr/bin/python
# -*- coding: utf-8 -*-

################################################################################

import urllib
import logging

from sourcecodeonline.classes.CustomHTMLParser import CustomHTMLParser

################################################################################

def stripPage(page):
    
    beginIndex = page.find('<table width="100%" border="0" class="list-view" cellspacing="0" cellpadding="0"><tr><th><nobr><big>')
    if beginIndex != -1:
        
        endIndex = page.find('</td></tr></table>', beginIndex)
        if endIndex != -1:
            return page[beginIndex : endIndex]

    return ''

################################################################################

url = 'http://www.sourcecodeonline.com/' 

logging.info('Scraping URL: ' + url)

page = urllib.urlopen(url).read()
page = stripPage(page)

if len(page) != 0:
    
    htmlParser = CustomHTMLParser()
    htmlParser.feed(page)
    htmlParser.close()
        
logging.info('Done!')
