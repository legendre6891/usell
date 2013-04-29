#!/usr/bin/env python

import cgi
import os
import xml.etree.cElementTree as etree
from google.appengine.ext.webapp import template
from google.appengine.ext import webapp
from google.appengine.api import memcache
from google.appengine.api import urlfetch
from google.appengine.ext.webapp.util import run_wsgi_app
import facebook
from google.appengine.api import users
import webapp2

from model import *


## API Keys go here!
_FbApiKey = '284783798323209'
_FbSecret = '488d93b118272ac03038445c1f4c3c15'

class MainPage(webapp.RequestHandler):
    def get(self):
        
        products = []
        errors = []
    
        ## instantiate the Facebook API wrapper with your FB App's keys
        fb = facebook.Facebook(_FbApiKey, _FbSecret)
    
        ## check that the user is logged into FB and has added the app
        ## otherwise redirect to where the user can login and install
        if fb.check_session(self.request) and fb.added:
            pass
        '''
        else:
            url = fb.get_add_url()
            self.response.out.write('<script language="javascript">top.location.href="' + url + '"</script>')
            return
        '''
        path = os.path.join(os.path.dirname(__file__), 'main.html')
        self.response.out.write(template.render(path, {}))


        # read in content from input box
        # input must be of form:
        #
        # college
        # first last
        # item

        content = self.request.get("content").split()
        
        # parse input
        if len(content) != 4:
            self.response.out.write("Invalid entry")

        else:
            collegeName   = content[0]
            userFirstName = content[1]
            userLastName  = content[2]
            itemName      = content[3]

            # create db entries, store them if they're new

            # TODO:
            # set up appropriate hierarchy:
            # user parent should be college, item parent should
            # be user.

            college = Network(name = collegeName)
            if college.exists() == None:
                Network.put(college)
            else:
                college = college.exists()

            user = User(firstName = userFirstName,
                lastName = userLastName)
            if not user.exists():
                User.put(user)

            item = Item(name = itemName)
            if not item.exists():
                Item.put(item)
    def post(self):
        self.get()



class FeedMe(webapp.RequestHandler):
    """
    """
    def get(self):
        self.response.write('<html><body>You wrote:<pre>')
        # self.response.write(cgi.escape(self.request.get('content')))
        self.response.write(cgi.escape(self.request.path))
        self.response.write('</pre></body></html>')


application = webapp.WSGIApplication(
                                     [('/', MainPage),
                                      ('/stuff.*', FeedMe),],
                                     debug=True)


def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    main()
