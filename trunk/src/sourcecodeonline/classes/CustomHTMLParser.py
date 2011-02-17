import logging
import string
import re

from datetime import datetime
from HTMLParser import HTMLParser

from SourceCodeOnlineFeedItem import SourceCodeOnlineFeedItem


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
        
        self.lastClassAttribute = ''
        
    """
    """
    def setLastClassAttribute(self, attrs):
        
        if attrs.has_key('class'):
            self.lastClassAttribute = attrs['class']
    
    """
    """
    def isItemStart(self, tag, attrs):
        
        if tag.lower() == 'h3':
            return True
        
        return False
    
    """
    """
    def isItemLink(self, tag, attrs):
        
        if self.isItemOpened:
            if tag.lower() == 'a':
                if attrs['class'] == 'source-name':
                    return True
            
        return False
       
    """
    """
    def isItemEnd(self, tag):
        
        return tag.lower() == 'p' and self.isItemOpened
    
    """
    """
    def isItemTitle(self):
        
        if self.isItemOpened:
            if self.currentPath.endswith('/div/a'):
                if self.lastClassAttribute == 'source-name':
                    return True
            
        return False
    
    """
    """
    def isItemDescription(self):
        
        if self.isItemOpened:
            if self.currentPath.endswith('/p'):
                return True
                
        return False
    
    """
    """
    def isItemDescriptionEnd(self, tag):
        
        return tag.lower() == 'p' and self.isItemOpened
    
    """
    """
    def isItemNew(self):
        
        feedItems = SourceCodeOnlineFeedItem.gql("WHERE link = :1", self.itemLink)
        if feedItems.count() == 0: 
            return True
       
        return False
   
    """
    """
    def saveItem(self):
        
        if self.isItemNew() == True:
            
            feedItem = SourceCodeOnlineFeedItem()
            
            feedItem.title       = self.itemTitle.strip().decode('utf-8')
            feedItem.link        = self.itemLink
            feedItem.description = self.itemDescription.decode('utf-8')
            
            feedItem.put()
            logging.info('Saving item: ' + feedItem.title)
        """    
        else:
            
            raise Exception()
        """
               
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
            self.itemLink = 'http://www.sourcecodeonline.com' + attrs['href']
        
        self.setLastClassAttribute(attrs)
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
        
        if self.isItemDescriptionEnd(tag):
            self.itemDescription += '<br />\n'
            
        if self.isItemEnd(tag):
            self.saveItem()
            self.resetItemData()
