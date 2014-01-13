#!/usr/bin/env python
# -*- coding:utf-8 -*- 
# Copyright 2014 FleeBuy All Right Reserved.

from HTMLParser import HTMLParser

# import webapp2 # from GAE
import json
import urllib2

import cgi
import datetime
import wsgiref.handlers
import rest

from google.appengine.api import users
from google.appengine.ext import webapp
from google.appengine.ext import db
from google.appengine.ext.webapp.util import run_wsgi_app

import models
from google.appengine.api import search 
_INDEX_NAME_ALL = 'search_all'
    
class MLStripper(HTMLParser):
    def __init__(self):
        self.reset()
        self.fed = []
    def handle_data(self, d):
        self.fed.append(d)
    def get_data(self):
        return ''.join(self.fed)

def strip_tags(html):
    s = MLStripper()
    s.feed(html)
    return s.get_data()

class MainHandler(webapp.RequestHandler):
    def get(self):
        #http://stackoverflow.com/questions/8464391/what-should-i-do-if-socket-setdefaulttimeout-is-not-working
        
        url='http://pipes.yahoo.com/pipes/pipe.run?_id=29604671a0cf78378f569387a5100e39&_render=json'
        response = urllib2.urlopen(url, timeout=40000) #try to resolove the request timeout issue
        data = response.read()
        json_data = json.loads(data)
        items = json_data.get('value')['items']
        
        for item in items:
            item_author_name = item.get('author')['name']
            item_title = item.get('title')
            item_link = item.get('link')

			# ===== get price from item description =====
            item_description = item.get('description')['content']
            item_description_strip = strip_tags(item_description)

            item_price_start = item_description_strip.find(u'欲售價格')
            price_start = item_price_start+len(u'欲售價格')
            
            possible_end_words = [u'售出原因', u'交易方式']
            price_end = -1
            for word in possible_end_words:
                price_end = item_description_strip[price_start:].find(word)
                if price_end != -1: break
            
            item_price = item_description_strip[price_start:price_start+price_end]
            char_should_not_exist = [' ', ':', u'：']
            for char in char_should_not_exist:
                item_price = item_price.replace(char, '')
			# ===========================================
            self.response.out.write('item_author_name: '+item_author_name+'<br>')
            self.response.out.write('item_title: '+item_title+'<br>')
            self.response.out.write('item_link: '+item_link+'<br>')
            self.response.out.write('item_price: '+item_price+'<br>')

            qry_item = db.GqlQuery("SELECT * FROM Item WHERE item_link=:1 LIMIT 1", item_link).get()
            
            #check data is exist in db or not
            if qry_item != None:
                self.response.out.write('isExist: Yes <br>')
            else:
                self.response.out.write('isExist: No <br>')
                item = models.Item()
                item.item_title = item_title
                item.item_author_name = item_author_name
                item.item_link = item_link
                item.item_description_strip = item_description_strip
                item.item_price = item_price
                
                document = search.Document(
                    doc_id=item_link,
                    fields=[search.TextField(name='item_title', value=item_title),
                            search.TextField(name='item_description_strip', value=item_description_strip),
                            search.TextField(name='item_price', value=item_price, language='zh')],
                    language='zh')
                
                try:
                    index = search.Index(name="_INDEX_NAME_ALL")
                    index.put(document)
                except search.Error:
                    logging.exception('Index Put failed')
                    
                item.put()
            self.response.out.write('<br><hr>')
            
class KeywordSearchHandler(webapp.RequestHandler):
# https://developers.google.com/appengine/docs/python/apis
# http://www.keakon.net/2012/05/09/GAE%E5%B7%B2%E6%94%AF%E6%8C%81%E4%B8%AD%E6%96%87%E5%85%A8%E6%96%87%E6%90%9C%E7%B4%A2
# http://fts-webinar.appspot.com/#1
# https://developers.google.com/appengine/training/fts_intro/lesson2
# https://github.com/GoogleCloudPlatform/appengine-search-python-java
    def get(self):
        k1 = self.request.get("k1")
        k2 = self.request.get("k2")
        k3 = self.request.get("k3")
        
        self.response.out.write('k1: '+k1+'<br>')
        self.response.out.write('k2: '+k2+'<br>')
        self.response.out.write('k3: '+k3+'<br>')
        self.response.out.write('<br><hr>')
        
        try:
            index = search.Index(name="_INDEX_NAME_ALL")
            search_results = index.search(k1)
            if search_results.number_found:
                for doc in search_results:
                    self.response.out.write('doc_id: '+doc.doc_id+'<br>')
                    self.response.out.write('item_title: '+doc.field('item_title').value+'<br>')
#                     self.response.out.write( doc.fields ) )
                    self.response.out.write('<br><hr>')
            else:
                self.response.out.write('0 result')
        except search.Error:
            self.response.out.write('search.Error at KeywordSearchHandler')

application = webapp.WSGIApplication([
    ('/', MainHandler),
    ('/keyword', KeywordSearchHandler),
    ('/rest/.*', rest.Dispatcher)
], debug=True)


# configure the rest dispatcher to know what prefix to expect on request urls
rest.Dispatcher.base_url = "/rest"

# add all models from the current module, and/or...
# rest.Dispatcher.add_models_from_module(__name__)

# add specific models
rest.Dispatcher.add_models({"Item": models.Item})

def main():
#   wsgiref.handlers.CGIHandler().run(application)
    run_wsgi_app(application)


if __name__ == '__main__':
    main()

