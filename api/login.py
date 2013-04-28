#!/usr/bin/python

import cookielib
import os.path
import sys
import urllib2
import urllib

######
# PARAMETERS TO EDIT
#SATELLITE_URL      = "http://satellite.example.com/rpc/api"
SATELLITE_URL      = "https://sat1.home.org/rhn/Login.do"
LOGIN_URL      = "https://sat1.home.org//rhn/ReLoginSubmit.do"
SATELLITE_LOGIN    = "admin"
SATELLITE_PASSWORD = "redhat"
######

# Set up cookie handling. We store cookies in the COOKIEFILE.
COOKIEFILE = "cookies.lwp"
cookieJar = cookielib.LWPCookieJar()
if os.path.isfile(COOKIEFILE):
  cookieJar.load(COOKIEFILE)

# Set up the handlers for the OpenerDirector. We need
# handlers for:
# -cookies;
# -HTTP digest authentication.
cookie_handler = urllib2.HTTPCookieProcessor(cookieJar)
#auth_handler = urllib2.HTTPBasicAuthHandler()
#auth_handler = urllib2.HTTPDigestAuthHandler()
#auth_handler.add_password(realm='trac',
                          #uri=SATELLITE_URL,
                          #user=SATELLITE_LOGIN,
                          #passwd=SATELLITE_PASSWORD)

# Build the OpenerDirector with the build_opener convenience
# method.
#opener = urllib2.build_opener(cookie_handler, auth_handler)
opener = urllib2.build_opener(cookie_handler)

# Install the OpenerDirector as the global default handler.
urllib2.install_opener(opener)

values = {
  'username': SATELLITE_LOGIN,
  'password': SATELLITE_PASSWORD,
  'login_cb': 'login',
  'url_bounce': '%2Frhn%2F',
}

urlencodedValues = urllib.urlencode(values)
try:
  response = urllib2.urlopen(LOGIN_URL, data=urlencodedValues)
  error = 0
except urllib2.HTTPError, e:
  print "Received HTTPError: ", e.code
  error = 1
except urllib2.URLError, e:
  print "Received URLError: ", e.code
  error = 1
if error: sys.exit(1)

#print response.geturl()
#print response.info()
print response.read()

