#!/usr/bin/python
# -*- coding: utf-8 -*-
##############################################################################
# WeatherStats
# Tiny Python scripts for general weather data management and analysis (with Netatmo support)
# (C) 2015-2016, Ulrich Thiel
# thiel@mathematik.uni-stuttgart.de
##############################################################################

##############################################################################
#This script contains basic functions for Netatmo API connection
#To a large extend taken from Philippe Larduinat, https://github.com/philippelt/netatmo-api-python/blob/master/lnetatmo.py

import json
import sys
import time

#HTTP libraries depends upon Python 2 or 3
if sys.version_info.major == 3 :
    import urllib.parse, urllib.request
else:
    from urllib import urlencode
    import urllib2
    

import pprint

##############################################################################
#Retrieves the device data for an account in JSON format
def postRequest(url, params):
    if sys.version_info.major == 3:
        req = urllib.request.Request(url)
        req.add_header("Content-Type","application/x-www-form-urlencoded;charset=utf-8")
        params = urllib.parse.urlencode(params).encode('utf-8')
        resp = urllib.request.urlopen(req, params).readall().decode("utf-8")
    else:
        params = urlencode(params)
        headers = {"Content-Type" : "application/x-www-form-urlencoded;charset=utf-8"}
        req = urllib2.Request(url=url, data=params, headers=headers)
        resp = urllib2.urlopen(req).read()
    return json.loads(resp)
    

##############################################################################
#Netatmo class
class NetatmoClient:
	
	#Netatmo URLs
	BASE_URL       = "https://api.netatmo.net/"
	AUTH_REQ       = BASE_URL + "oauth2/token"
	GETUSER_REQ    = BASE_URL + "api/getuser"	#deprecated
	DEVICELIST_REQ = BASE_URL + "api/devicelist"	#deprecated
	GETSTATION_REQ = BASE_URL + "api/getstationsdata"
	GETMEASURE_REQ = BASE_URL + "api/getmeasure"
	
	def __init__(self, username, password, clientId, clientSecret):
		
		self.username = username
		self.password = password
		self.clientId = clientId
		self.clientSecret = clientSecret
		
		postParams = {
                "grant_type" : "password",
                "client_id" : clientId,
                "client_secret" : clientSecret,
                "username" : username,
                "password" : password,
                "scope" : "read_station"
                }
                       
		resp = postRequest(self.AUTH_REQ, postParams)
		self.accessToken = resp['access_token']
		self.refreshToken = resp['refresh_token']
		self.scope = resp['scope']
		self.expiration = int(resp['expire_in'] + time.time())
		
	#function for refreshing access token if necessary
	def refreshAccessToken(self):

		if self.expiration < time.time(): # Token should be renewed

			postParams = {
                    "grant_type" : "refresh_token",
                    "refresh_token" : self.refreshToken,
                    "client_id" : self.clientId,
                    "client_secret" : self.clientSecret
                    }
			resp = postRequest(self.AUTH_REQ, postParams)

			self.accessToken = resp['access_token']
			self.refreshToken = resp['refresh_token']
			self.expiration = int(resp['expire_in'] + time.time())
			
	def getDeviceList(self):
		
		self.refreshAccessToken()	#will only do if necessary
		postParams = {"access_token" : self.accessToken}
		resp = postRequest(self.GETSTATION_REQ, postParams)
		raw = resp['body']
		self.deviceList = raw['devices']
		print pprint.pprint(resp)
        
        
netatm = NetatmoClient("globalproj@gmx.net", "JKvser4", "56c0990d65d1c4e1a3b08f4a", "3wA2Vf64jEK06LOtZLbA6Krlv0NIHDq")

netatm.getDeviceList()