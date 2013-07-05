#!/usr/bin/env python

#
# A Python Program to Get the Weather Info Using Yahoo Web Services
# Copyright (C) 2013 Saurav Haloi [sauravhaloi4@gmail.com]
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#

#
# * Steps :
# * Accept the name of the city from command line
# * Using Yahoo Map API, get the latitude & longitude of the city
# * Get the WOEID (Where On Earth ID) of the city with the latutide & longitude by using Flickr API
# * Use the WOEID to get the Weather info of the city through Yahoo Weather API
#

import os
import sys
import urllib
import urllib2
import xml.dom.minidom

from urllib2 import Request, urlopen, URLError
from xml.dom import Node
from xml.etree import ElementTree

def clearScreen():
    if os.name == "posix":
        os.system("clear")
    elif os.name in ("nt", "dos", "ce"):
        os.system("cls")

def printLatLonInfo(CITY):
    MyAppID="fmIN.drV34HOC8FaDjSoo6ArkYvtwg1p8WYMf2xnUVBPqHTZkq4raMB0_0.1NcRV.AaKHFoa"
    LatLonURL="http://local.yahooapis.com/MapsService/V1/geocode?appid="+MyAppID+"&city="+CITY
    try:
        response=urllib2.urlopen(LatLonURL)
    except URLError, e:
        if hasattr(e, 'reason'):
            print 'We failed to reach a server.'
            print 'Reason: ', e.reason
        elif hasattr(e, 'code'):
            print 'The server couldn\'t fulfill the request.'
            print 'Error code: ', e.code
    else:
        parseLatLonXML(response)

def parseLatLonXML(response):
    document=response.read()
    dom = xml.dom.minidom.parseString(document)
    Latitude = []
    Longitude = []
    City = []
    State = []
    Country = []
    for node in dom.getElementsByTagName('Latitude'):
        #print 'Latitude: ' + node.firstChild.nodeValue
        Latitude.append(node.firstChild.nodeValue)
    for node in dom.getElementsByTagName('Longitude'):
        Longitude.append(node.firstChild.nodeValue)
    for node in dom.getElementsByTagName('City'):
        City.append(node.firstChild.nodeValue)
    for node in dom.getElementsByTagName('State'):
        State.append(node.firstChild.nodeValue)
    for node in dom.getElementsByTagName('Country'):
        Country.append(node.firstChild.nodeValue)

    count = int(len(City))

    if count == 0:
        print "No Results Found"
        exit(1)
    else:
        print str(count) + " Results Found.\n"

    if count > 1:
        for i in range(0,count):
            print str(i) + ". " + City[i] + " " + State[i] + " " + Country[i]

        print '--------------------------------------'
        sys.stdout.write("Enter Your Choice :\t")
        choice = int(raw_input())

        if choice < 0 or choice >= count:
            print 'Error: Out Of Range !!! Exiting...'
            exit()
        else:
            print "### Weather Infomation for " + City[choice] + " " + State[choice] + " " + Country[choice] + " ###\n"
            print 'Latitude: ' + Latitude[choice]
            print 'Longitude: ' +  Longitude[choice]
            print 'City: ' + City[choice]
            print 'State: ' +  State[choice]
            print 'Country: ' +  Country[choice]
            woeid=findWOEID(Latitude[choice],Longitude[choice])
            print 'Where On Earth ID: ' + woeid + "\n"
            weather(woeid)
            print '--------------------------------------'
    else:
        count = count - 1
        print "### Weather Infomation for " + City[count] + " " + State[count] + " " + Country[count] + " ###\n"
        print 'Latitude: ' + Latitude[count]
        print 'Longitude: ' +  Longitude[count]
        print 'City: ' + City[count]
        print 'State: ' +  State[count]
        print 'Country: ' +  Country[count]
        woeid=findWOEID(Latitude[count],Longitude[count])
        print 'Where On Earth ID: ' + woeid + "\n"
        weather(woeid)
        print '--------------------------------------'

def findWOEID(lat,lon):
    WOEID_YQL="select%20place.woeid%20from%20flickr.places%20where%20lat%3D"+lat+"%20and%20lon%3D+"+lon
    WOEID_URL="http://query.yahooapis.com/v1/public/yql?q="+WOEID_YQL+"&diagnostics=true"
    try:
        response=urllib2.urlopen(WOEID_URL)
    except URLError, e:
        if hasattr(e, 'reason'):
            print 'We failed to reach a server.'
            print 'Reason: ', e.reason
        elif hasattr(e, 'code'):
            print 'The server couldn\'t fulfill the request.'
            print 'Error code: ', e.code
    else:
        #tree = ElementTree.parse(response)
        #node = tree.findall("/place")
        #for item in node:
            #print item

        document=response.read()
        dom = xml.dom.minidom.parseString(document)

        for node in dom.getElementsByTagName('place'):
            WOEID = node.getAttribute("woeid")

    return WOEID

def weather(woeid):
    WEATHER_URL="http://weather.yahooapis.com/forecastrss?w="+woeid+"&u=c"
    WEATHER_NS = 'http://xml.weather.yahoo.com/ns/rss/1.0'

    try:
        response=urllib2.urlopen(WEATHER_URL)
    except URLError, e:
        if hasattr(e, 'reason'):
            print 'We failed to reach a server.'
            print 'Reason: ', e.reason
        elif hasattr(e, 'code'):
            print 'The server couldn\'t fulfill the request.'
            print 'Error code: ', e.code
    else:
        dom = xml.dom.minidom.parse(response)

        for node in dom.getElementsByTagNameNS(WEATHER_NS, 'condition'):
            print 'Date: ' +  node.getAttribute('date') + "\n"
            print 'Current Condition: ' + node.getAttribute('text')
            print 'Current Temperature: ' + node.getAttribute('temp') + ' C'

        for node in dom.getElementsByTagNameNS(WEATHER_NS, 'atmosphere'):
            print "Humidity: " + node.getAttribute('humidity') + "%"

        for node in dom.getElementsByTagNameNS(WEATHER_NS, 'astronomy'):
            print "Sun Rise: " + node.getAttribute('sunrise')
            print "Sun Set: " + node.getAttribute('sunset')

        for node in dom.getElementsByTagNameNS(WEATHER_NS, 'forecast'):
            print "\n"
            print 'Forcast for Date: ' + node.getAttribute('day') + " " + node.getAttribute('date')
            print 'Minimum Temperature: ' + node.getAttribute('low') + ' C'
            print 'Maximum Temperature: ' + node.getAttribute('high') + ' C'
            print 'Condition: ' + node.getAttribute('text')

def main():
    clearScreen()
    if len(sys.argv) != 2:
        print "Usage: " + sys.argv[0] + " <Name of City>"
        exit(1)
    else:
        CITY = sys.argv[1]

    print "You Asked for Weather Information of city \"" + CITY + "\"."
    printLatLonInfo(CITY)
    print "Good Bye..."

main()
