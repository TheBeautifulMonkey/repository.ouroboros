# -*- coding: UTF-8 -*-

"""
 weblogin
 by Anarchintosh @ xbmcforums
 Copyleft (GNU GPL v3) 2011 onwards

 this example is configured for Fantasti.cc login
 See for the full guide please visit:
 http://forum.xbmc.org/showthread.php?p=772597#post772597


 USAGE:
 in your default.py put:

 import weblogin
 logged_in = weblogin.doLogin('a-path-to-save-the-cookie-to','the-username','the-password')

 logged_in will then be either True or False depending on whether the login was successful.
"""

import os
import re
import urllib,urllib2
import cookielib
import koding



def check_login(source,username):
    
    #the string you will use to check if the login is successful.
    #you may want to set it to:    username     (no quotes)
    logged_in_string = 'Welcome to '

    #search for the string in the html, without caring about upper or lower case
    if re.search(logged_in_string,source,re.IGNORECASE):
        return True
    else:
        return False


def doLogin(cookiepath, username, password):

    #check if user has supplied only a folder path, or a full path
    if not os.path.isfile(cookiepath):
        #if the user supplied only a folder path, append on to the end of the path a filename.
        cookiepath = os.path.join(cookiepath, 'cookies.lwp')
        
    #delete any old version of the cookie file
    try:
        os.remove(cookiepath)
    except:
        pass

    if username and password:

        #the url you will request to.
        login_url = 'http://laffinatcha.stream/login.php'

        #the header used to pretend you are a browser
        header_string = 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3'

	#build the form data necessary for the login
        login_data = urllib.urlencode({'username':username, 'password':password})

        #build the request we will make
        req = urllib2.Request(login_url, login_data)
        req.add_header('User-Agent',header_string)

        #initiate the cookielib class
        cj = cookielib.LWPCookieJar()

        #install cookielib into the url opener, so that cookies are handled
        opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))

        #do the login and get the response
        response = opener.open(req)
        source = response.read()
        response.close()

        #check the received html for a string that will tell us if the user is logged in
        #pass the username, which can be used to do this.
        login = check_login(source,username)

        #if login suceeded, save the cookiejar to disk
        if login == True:
            cj.save(cookiepath)

        #return whether we are logged in or not
        return login
    
    else:
        return False


