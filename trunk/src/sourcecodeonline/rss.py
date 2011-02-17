#!/usr/bin/python
# -*- coding: utf-8 -*-

################################################################################

import PyRSS2Gen
import sys

from datetime import date

from sourcecodeonline.classes.SourceCodeOnlineFeedItem import SourceCodeOnlineFeedItem

################################################################################

rss = PyRSS2Gen.RSS2(
        title = 'SourceCodeOnline.com - New Source List',
        link  = 'http://www.sourcecodeonline.com/',
        description = 'New Source List at SourceCodeOnline.com',
        generator = 'http://feedgenerator.appspot.com/',
        docs = ''
      )


today = date.today()
items = SourceCodeOnlineFeedItem.gql("ORDER BY pubDate DESC LIMIT 50")
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
