#!/usr/bin/python
# -*- coding: utf-8 -*-

################################################################################

import urllib
import logging

from vclcomponents.classes.CustomHTMLParser import CustomHTMLParser

################################################################################

def stripPage(page):
    
    beginIndex = page.find('<table border="0" cellpadding="3" cellspacing="3" id="LatestSoftware">')
    if beginIndex != -1:
        
        endIndex = page.find('</table>', beginIndex)
        if endIndex != -1:
            return page[beginIndex : endIndex]

    return ''

################################################################################

url = 'http://www.vclcomponents.com/new' 

logging.info('Scraping URL: ' + url)

page = urllib.urlopen(url).read()
page = stripPage(page)

if len(page) != 0:
    
    htmlParser = CustomHTMLParser()
    htmlParser.feed(page)
    htmlParser.close()
        
logging.info('Done!')
