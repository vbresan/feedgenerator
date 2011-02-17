#!/usr/bin/python
# -*- coding: utf-8 -*-

################################################################################

import PyRSS2Gen
import sys

from datetime import date

from filetransit.classes.FileTransitFeedItem import FileTransitFeedItem

################################################################################

rss = PyRSS2Gen.RSS2(
        title = 'FileTransit.com - New Software Downloads',
        link  = 'http://www.filetransit.com/',
        description = 'New Software Downloads at FileTransit.com',
        generator = 'http://feedgenerator.appspot.com/',
        docs = ''
      )


today = date.today()
items = FileTransitFeedItem.gql("ORDER BY pubDate DESC LIMIT 50")
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
