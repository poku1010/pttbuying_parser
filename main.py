#!/usr/bin/env python
# -*- coding:utf-8 -*- 
# Copyright 2007 Googlbig5e Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

from google.appengine.ext import ndb # from GAE
from HTMLParser import HTMLParser

import webapp2 # from GAE
import json
import urllib2
import socket #set a global timeout for all socket operations (including HTTP requests)

class Item(ndb.Model):
    #Models an individual item entry.
    #https://developers.google.com/appengine/docs/python/ndb/properties?hl=zh-tw
    item_title = ndb.StringProperty(indexed=False)
    item_author_name = ndb.StringProperty(indexed=False)
    item_link = ndb.StringProperty(indexed=True)
    item_description_strip = ndb.StringProperty(indexed=False)
    item_price = ndb.StringProperty(indexed=False)
    datetime = ndb.DateTimeProperty(auto_now_add=True)

class MainHandler(webapp2.RequestHandler):
    def get(self):
        #http://stackoverflow.com/questions/8464391/what-should-i-do-if-socket-setdefaulttimeout-is-not-working
        socket.setdefaulttimeout(300) #try to resolove the request timeout issue

        url='http://pipes.yahoo.com/pipes/pipe.run?_id=29604671a0cf78378f569387a5100e39&_render=json'
        response = urllib2.urlopen(url)
        data = response.read()
        json_data = json.loads(data)
        items = json_data.get('value')['items']
        
        for item in items:
            item_author_name = item.get('author')['name']
            item_title = item.get('title')
            item_link = item.get('link')

            item_description = item.get('description')['content']
            item_description_strip = strip_tags(item_description)

            item_price_start = item_description_strip.find(u'欲售價格')
            price_start = item_price_start+len(u'欲售價格')
            
            possible_end_words = [u'售出原因', u'交易方式']
            item_price_end = -1
            for word in possible_end_words:
                item_price_end = item_description_strip[price_start:].find(word)
                if item_price_end != -1: break
            
            # item_price_end = item_description_strip[price_start:].find(u'售出原因')
            # if item_price_end == -1:
                # item_price_end = item_description_strip[price_start:].find(u'交易方式')
            
            item_price = item_description_strip[price_start:price_start+item_price_end]
            char_should_not_exist = [' ', ':', u'：']
            for char in char_should_not_exist:
                item_price = item_price.replace(char, '')

            self.response.out.write('item_author_name: '+item_author_name+'<br>')
            self.response.out.write('item_title: '+item_title+'<br>')
            self.response.out.write('item_link: '+item_link+'<br>')
            self.response.out.write('item_price: '+item_price+'<br>')
            
            #https://developers.google.com/appengine/docs/python/ndb/queries
            qry = Item.query(Item.item_link == item_link)
            qry_item = qry.fetch(1)

            #check data is exist in db or not
            if qry_item:
                self.response.out.write('isExist: Yes <br>')
                
            else:
                self.response.out.write('isExist: No <br>')
                # We set the parent key on each 'items' to ensure each Source's
                # items are in the same entity group.
                item_db = Item(parent=ndb.Key('Source', 'PTT_mobilesales'),
                            item_title = item_title,
                            item_author_name = item_author_name,
                            item_link = item_link,
                            item_description_strip = item_description_strip,
                            item_price = item_price)
                item_db.put()

            self.response.out.write('<br><hr>')

                
            
            
        #self.response.write('PTT Buying Parser GAE.')
        #self.response.out.write(json_data)

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

app = webapp2.WSGIApplication([
    ('/', MainHandler)
], debug=True)

