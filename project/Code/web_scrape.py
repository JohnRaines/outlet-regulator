#**************************************************
#This file contains all the functions for pulling
#data from the http site and trim it to useable
#state
#
#Author: John Raines
#Date: 14 - 12 - 16 (dd mm yy)
#**************************************************

#imports
import urllib

#define the web address
SITE = "http://192.168.1.104"


#pulls the info currently on the site
def get_site():
    s = urllib.urlopen(SITE)
    nj = s.read()

    #salient info is index + 3 to index + 15
    index = nj.index("<p>")
    nj = nj[index+3:index+15]

    return nj
    
