#!/usr/bin/python
# -*- coding: utf-8 -*-

################################################################################

import PyRSS2Gen
import sys

from datetime import date

from filehungry.classes.FileHungryFeedItem import FileHungryFeedItem

################################################################################

rss = PyRSS2Gen.RSS2(
        title = 'FileHungry.com - New products',
        link  = 'http://www.filehungry.com/',
        description = 'New products at FileHungry.com',
        generator = 'http://feedgenerator.appspot.com/',
        docs = ''
      )


today = date.today()
items = FileHungryFeedItem.gql("ORDER BY pubDate DESC LIMIT 50")
for item in items:
    rss.items.append(PyRSS2Gen.RSSItem(
                                                
            title       = item.title, 
            link        = item.link,
#            description = '<![CDATA[' + item.description + ']]>',
            description = item.description,
            pubDate     = item.pubDate
        ))

print 'Content-Type: application/rss+xml'
rss.write_xml(sys.stdout, 'utf-8')
