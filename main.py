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

from google.appengine.ext import ndb
from HTMLParser import HTMLParser

import webapp2
import json
import urllib2

class Item(ndb.Model):
    #Models an individual item entry with title, keyword, price, and date.
    title = ndb.StringProperty(indexed=False)
    content = ndb.StringProperty(indexed=False)
    price = ndb.StringProperty(indexed=False)
    datetime = ndb.DateTimeProperty(auto_now_add=True)

class MainHandler(webapp2.RequestHandler):
    def get(self):
    	url='http://pipes.yahoo.com/pipes/pipe.run?_id=29604671a0cf78378f569387a5100e39&_render=json'
    	response = urllib2.urlopen(url)
        data = response.read()
        json_data = json.loads(data)
        items = json_data.get('value')['items']
        
        for item in items:
		    item_author_name = item.get('author')['name']
		    #author_name = author.get('name')
		    item_title = item.get('title')
		    item_link = item.get('link')

		    item_description = item.get('description')['content']
		    item_description_strip = strip_tags(item_description)

		    item_price_start = item_description_strip.find(u'售價格：')
		    price_start = item_price_start+len(u'售價格：')
		    item_price_end = item_description_strip[price_start].find(u' ')
		    item_price = item_description_strip[price_start:]

		    self.response.out.write(item_price)
		    self.response.out.write('<br><hr>')
		    
		    #campaignID = item.get("CampaignID")

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

