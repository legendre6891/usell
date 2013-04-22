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

    def post(self):
        self.get()




application = webapp.WSGIApplication(
                                     [('/', MainPage),],
                                     debug=True)

def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    main()