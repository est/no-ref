#!/usr/bin/env python
#coding: utf-8




from google.appengine.ext import webapp
from google.appengine.ext.webapp import util
from urllib import unquote as url_unquote
import re, os

class homepage(webapp.RequestHandler):

    def get(self):
        self.response.out.write(open('index.html').read())

class gfw(webapp.RequestHandler):
    pass

class jump(webapp.RequestHandler):
    
    def get(self, url):
        r=re.search(r'^http://(.*)$', self.request.url)
        is_dev = os.environ['SERVER_SOFTWARE'][:3]
        if r and is_dev!='Dev':
            self.redirect('https://'+r.groups()[0], permanent=True)
        else:
            r=re.search(r'(http.?://.*$)', url_unquote(url))
            if r:
                self.redirect(r.groups()[0], permanent=True)
            else:
                self.response.set_status(400)
                self.response.out.write(url)


def main():
    application = webapp.WSGIApplication([
        ('/', homepage),
        ('/gfw(.*)', gfw),
        # TODO: more features
        ('(.*)', jump),
        ], debug=True)
    util.run_wsgi_app(application)


if __name__ == '__main__':
    main()
