##    Shelftalkers
##    Copyright 2008 Omar Abdelwahed
##
##    This file is part of Shelftalkers.
##
##    Shelftalkers is free software: you can redistribute it and/or modify
##    it under the terms of the GNU General Public License as published by
##    the Free Software Foundation, either version 3 of the License, or
##    (at your option) any later version.
##
##    Shelftalkers is distributed in the hope that it will be useful,
##    but WITHOUT ANY WARRANTY; without even the implied warranty of
##    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
##    GNU General Public License for more details.
##
##    You should have received a copy of the GNU General Public License
##    along with Shelftalkers.  If not, see <http://www.gnu.org/licenses/>.

import cgi
import os
import xml.etree.cElementTree as etree
from google.appengine.ext.webapp import template
from google.appengine.ext import webapp
from google.appengine.api import memcache
from google.appengine.api import urlfetch
from google.appengine.ext.webapp.util import run_wsgi_app
import facebook
from facebook import FacebookError

## API Keys go here!
_FbApiKey = '583839298302474'
_FbSecret = '9b892268aef38e50b14743c1ebda32bc'
_BestBuyRemixKey = 'your Remix key here'
_iLikeDevKey = 'your iLike key here'

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
    else:
       url = fb.get_add_url()
       self.response.out.write('<script language="javascript">top.location.href="' + url + '"</script>')
       return
    
    ## check for a search request
    if self.request.get('p'):

      ## get the product to search for and the original text comment
      ## from the submit form
      product = self.request.get('p').replace(' ','%20') ## encode spaces with %20
      txt = self.request.get('t')

      ## show: filter that specifies exact attributes to return.
      ## remove if you want everything
      f = '&show=sku,productId,name,artistName,type,regularPrice,salePrice,url,thumbnailImage,inStoreAvailability,onlineAvailability'

      ## example search parameters for Music products only and
      ## artist by name. You can search against any legal attribute in
      ## the Remix product set. Replace with whatever you want.
      ## Note the wildcard '*'. It lets you search on
      ## partial artist name strings.
      search = 'artistName=\'' + product + '*\'&type=\'Music\''

      ## the complete API url we'll call
      url = 'http://api.remix.bestbuy.com/v1/products(' + search + ')?&apiKey=' + _BestBuyRemixKey + f;

      ## call product search api
      try:
        result = urlfetch.fetch(url)
        if result.status_code == 200:

          ## parse XML return
          dom = etree.fromstring(result.content)

          ## build list of returned products by traversing parsed XML
          items = dom.findall('.//product')
          for item in items:
            dat = {
                'sku'         : item.findtext('.//sku/*'),
                'productId'  : item.findtext('.//productId'),
                'name': item.findtext('.//name'),
                'artistName': item.findtext('.//artistName'),
                'type'    : item.findtext('.//type'),
                'regularPrice'      : item.findtext('.//regularPrice'),
                'salePrice'      : item.findtext('.//salePrice'),
                'bbyUrl'      : item.findtext('.//url'),
                'thumbnailImage'      : item.findtext('.//thumbnailImage'),
                'inStoreAvailability'      : item.findtext('.//inStoreAvailability'),
                'onlineAvailability'      : item.findtext('.//onlineAvailability'),
                'text'      : txt,
                }
            products.append(dat)

        else:
          er = {'desc': '%s' % result.status_code,}
          errors.append(er)

      except DownloadError, e:
        er = {'desc': '%s' % e,}
        errors.append(er)

    params = ""
    for key in self.request.params.keys():
      if key != 'p' and key != 't':
        if params == "":
          params = key + "=" + self.request.get(key)
        else:
          params += "&" + key + "=" + self.request.get(key)
        
    ## build template values containing products (or errors) for index.html  
    template_values = {
      'iLikeDevKey': _iLikeDevKey,
      'products': products,
      'errors': errors,
      'params': params,
      }

    ## redirect to index.html and pass template values
    path = os.path.join(os.path.dirname(__file__), 'index.html')
    self.response.out.write(template.render(path, template_values))

application = webapp.WSGIApplication(
                                     [('/', MainPage)],
                                     debug=True)

def main():
  run_wsgi_app(application)

if __name__ == "__main__":
  main()
