import logging
import string
import re

from datetime import datetime
from HTMLParser import HTMLParser

from ComponentSourceFeedItem import ComponentSourceFeedItem


"""
"""
class CustomHTMLParser(HTMLParser):
    
    """
    
    
    """
    def resetItemData(self):
        
        self.isItemOpened    = False
        self.itemTitle       = ''
        self.itemLink        = ''
        self.itemDescription = ''
        
    """
    
    
    """
    def isItemStart(self, tag, attrs):
        
        if tag.lower() == 'li':
            return True
        
        return False
    
    """
    
    
    """
    def isItemLink(self, tag, attrs):
        
        if self.isItemOpened:
            if tag.lower() == 'a':
                if self.currentPath == '/ul/li/h3':
                    return True
            
        return False
       
    """
    
    
    """
    def isItemEnd(self, tag):
        
        if tag.lower() == 'li':
            if self.isItemOpened:
                return True
            
        return False
    
    """
    
    
    """
    def isItemTitle(self):
        
        if self.isItemOpened:
            if self.currentPath == '/ul/li/h3/a':
                return True
            
        return False
    
    """
    
    
    """
    def isItemDescription(self):
        
        if self.isItemOpened:
            if self.currentPath == '/ul/li/p/span':
                return True
                
        return False
    
    """
    
    
    """
    def isItemNew(self):
        
        feedItems = ComponentSourceFeedItem.gql("WHERE link = :1", self.itemLink)
        if feedItems.count() == 0: 
            return True
       
        return False
   
    """
    
    
    """
    def saveItem(self):
        
        if self.isItemNew() == True:
            
            feedItem = ComponentSourceFeedItem()
            
            feedItem.title       = self.itemTitle.strip().decode('utf-8')
            feedItem.link        = self.itemLink
            feedItem.description = self.itemDescription.strip().decode('utf-8')
            
            feedItem.put()
            logging.info('Saving item: ' + feedItem.title)
               
    """
    """
    def __init__(self):
        HTMLParser.__init__(self)

        self.currentPath = ''
        self.resetItemData()
        
        logging.info('Parsing page.')

    """
    """
    def handle_starttag(self, tag, attrs):
        
        attrs = dict(attrs)
        
        if self.isItemStart(tag, attrs):
            self.isItemOpened = True
            
        if self.isItemLink(tag, attrs):
            self.itemLink = 'http://www.componentsource.com' + attrs['href']
        
        self.currentPath += '/' + tag
        
    """
    """
    def handle_entityref(self, entity):
        
        if entity == 'amp':
            if self.isItemTitle():
                self.itemTitle = self.itemTitle.rstrip() + ' &amp;'
            elif self.isItemDescription():
                self.itemDescription = self.itemDescription.rstrip() + ' &amp;'

    """
    """
    def handle_data(self, data):
        
        if self.isItemTitle():
            self.itemTitle += data + ' '
        elif self.isItemDescription():
            self.itemDescription += data + ' '
        
    """
    """
    def handle_endtag(self, tag):

        self.currentPath = string.rsplit(self.currentPath, '/', 1)[0]
        
        if self.isItemEnd(tag):
            self.saveItem()
            self.resetItemData()
