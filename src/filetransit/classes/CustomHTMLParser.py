import logging
import string
import re

from datetime import datetime
from HTMLParser import HTMLParser

from FileTransitFeedItem import FileTransitFeedItem


"""
"""
class CustomHTMLParser(HTMLParser):
    
    """
    
    OK
    
    """
    def resetItemData(self):
        
        self.isItemOpened    = False
        self.itemTitle       = ''
        self.itemLink        = ''
        self.itemDescription = ''
    
    """
    
    OK
    
    """
    def isItemStart(self, tag, attrs):
        
        if tag.lower() == 'div':
            if attrs.has_key('class') and attrs.has_key('style'):
                if attrs['class'] == 'story':
                    if attrs['style'] == 'background-color:#EEF1F6;': 
                        return True
                    elif attrs['style'] == 'background-color:#E4E7EC;':
                        return True
        
        return False
    
    """
    
    OK
    
    """
    def isItemLink(self, tag, attrs):
        
        if self.isItemOpened:
            if tag.lower() == 'a':
                if self.currentPath.endswith('div'):
                    if attrs['class'] == 'capsule2':
                        return True
            
        return False
       
    """
    
    OK
    
    """
    def isItemEnd(self, tag):
        
        if tag.lower() == 'table':
            if self.isItemOpened:
                return True
            
        return False
    
    """
    
    OK
    
    """
    def isItemTitle(self):
        
        if self.isItemOpened:
            if self.currentPath.endswith('/div/a/strong'):
                return True
            
        return False
    
    """
    
    OK
    
    """
    def isItemDescription(self):
        
        if self.isItemOpened:
            if self.currentPath.endswith('/p'):
                return True
                
        return False
    
    """
    
    OK
    
    """
    def isItemNew(self):
        
        feedItems = FileTransitFeedItem.gql("WHERE link = :1", self.itemLink)
        if feedItems.count() == 0: 
            return True
       
        return False
   
    """
    
    OK
    
    """
    def saveItem(self):
        
        if self.isItemNew() == True:
            
            feedItem = FileTransitFeedItem()
            
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
        elif self.isItemLink(tag, attrs):
            self.itemLink = 'http://www.filetransit.com' + attrs['href']
        
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
