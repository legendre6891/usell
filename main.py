#!/usr/bin/env python

import cgi
import os
import xml.etree.cElementTree as etree
from google.appengine.ext.webapp import template
from google.appengine.ext import webapp
from google.appengine.api import memcache
from google.appengine.api import urlfetch
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.api import users
import webapp2

from model import *

# Import for data storage
from google.appengine.ext import db


class AdvancedSell(db.Model):
    # Item Name
    itemName = db.StringProperty(required=False)
    # Price of Item
    price = db.StringProperty(required=False)
    # Description of Item
    description = db.StringProperty(required=False)
    # Image of item
    image = db.StringProperty(required=False)
    # Category of item
    category = db.StringProperty(required=False)
    
    # Identifies when message was posted
    when = db.DateTimeProperty(auto_now_add=True)

    

class MainPage(webapp.RequestHandler):
    def get(self):
        sellposts = db.GqlQuery(
                             'SELECT * FROM AdvancedSell '
                             'ORDER BY when DESC')
        values = {'sellposts':sellposts}
        
        # Uncomment this to delete all material in data store
        #db.delete(sellposts)

        path = os.path.join(os.path.dirname(__file__), 'main.html')
        self.response.out.write(template.render(path,values))
    
    #self.redirect('/')

    def post(self):
        self.get()
        itemName = AdvancedSell(itemName=self.request.get('itemName'), \
                         price=self.request.get('price'), \
                         description=self.request.get('description'), \
                         image=self.request.get('image'), \
                         category=self.request.get('category'), )
        # Puts it in the data store
        itemName.put()
        # Redirect user to main page
        self.redirect('/')


application = webapp.WSGIApplication(
                                     [('/', MainPage),],
                                     debug=True)

def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    main()