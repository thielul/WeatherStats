#!/usr/bin/python
# -*- coding: utf-8 -*-
##############################################################################
# WeatherStats
# A collection of Python scripts for general weather data management and analysis with Netatmo support
# (C) 2015-2016, Ulrich Thiel
# thiel@mathematik.uni-stuttgart.de
##############################################################################

##############################################################################
#This file contains some functions to convert timestamps to usual date formats and conversely

import datetime
import calendar
import time
from pytz import timezone

#Current timestamp
def CurrentTimestamp():
	return int(time.time())

#Returns the datetime in format YYYY-mm-dd HH:MM:SS
def DatetimeFromTimestamp(t,tz):
	if tz != None:
		tz = timezone(tz)
	return datetime.datetime.fromtimestamp(t,tz).strftime('%Y-%m-%d %H:%M:%S')
	
#Returns the date in format Y-m-d from a datetime 
def DateFromDatetime(s):
	return s[0:10]
	 
#Returns the day in format Y-m-d Hh from a datetime
def DateHourFromDatetime(s):
	return s[0:13]+"h"
	
#Returns the year from a datetime
def YearFromDatetime(s):
	return int(s[0:4])
	
#Returns the month from a datetime
def MonthFromDatetime(s):
	return int(s[5:7])
	
#Returns the day from a datetime
def DayFromDatetime(s):
	return int(s[8:10])	
	
#Returns the month from a datetime
def HourFromDatetime(s):
	return int(s[11:13])
	
#Returns the minute from a datetime
def MinuteFromDatetime(s):
	return int(s[14:16])

#Returns the second from a datetime
def SecondFromDatetime(s):
	return int(s[17:19])
		
#Returns first timestamp of date s (s in format Y-m-d)
def FirstTimestampOfDate(s):
	return time.mktime(datetime.datetime.strptime(s, "%Y-%m-%d").timetuple())
	
#Returns last timestamp of date s (s in format Y-m-d)
def LastTimestampOfDate(s):
	return time.mktime((datetime.datetime.strptime(s, "%Y-%m-%d") + datetime.timedelta(1)).timetuple() )
	
#Returns first timestamp of year s
def FirstTimestampOfYear(s):
	return FirstTimestampOfDate(s+"-01-01")
	
#Returns last timestamp of year s
def LastTimestampOfYear(s):
	return LastTimestampOfDate(s+"-12-31")
	
#Returns first timestamp of month m of year y
def FirstTimestampOfMonth(y,m):
	return FirstTimestampOfDate(str(y)+"-"+str(m)+"-01")

#Returns last date of month m of year y
def LastDayOfMonth(y,m):
	return calendar.monthrange(y,m)[1]
	
#Returns first timestamp of month m of year y
def LastTimestampOfMonth(y,m):
	return LastTimestampOfDate(str(y)+"-"+str(m)+"-"+str(LastDayOfMonth(y,m)))
		
#Returns first timestamp of datetime s (s in format Y-m-d H:m)
def TimestampOfDatetime(s):
	return time.mktime(datetime.datetime.strptime(s, "%Y-%m-%d %H:%M").timetuple())


##############################################################################
# the number of days between end and start (given in format Y-m-d)
def NumberOfDaysBetween(start, end):
	date_format = "%Y-%m-%d"
	a = datetime.datetime.strptime(start, date_format)
	b = datetime.datetime.strptime(end, date_format)
	delta = b - a
	return delta.days 
	
##############################################################################
def GetDateHours(years, months, days, hours, start, end):
	
	if start is not None:
		startdate = datetime.datetime.strptime(start, "%Y-%m-%d")
		startyear = startdate.year
		startmonth = startdate.month
		startday = startdate.day
	
	if end is not None:
		enddate = datetime.datetime.strptime(end, "%Y-%m-%d")
		endyear = enddate.year
		endmonth = enddate.month
		endday = enddate.day
		
	if start is None:
		if years is not None:
			startyear = min(years)
		else:
			if endyear is not None:
				startyear = endyear
			else:
				raise MyError('Cannot determine date range')
		if months is not None:
			startmonth = min(months)
		else:
			startmonth = 1
		
		if days is not None:
			startday = min(days)
		else:
			startday = 1
			
		startdate = datetime.datetime.strptime(str(startyear)+"-"+str(startmonth)+"-"+str(startday), "%Y-%m-%d")
			
	if end is None:
		if years is not None:
			endyear = max(years)
		else:
			if startyear is not None:
				endyear = startyear
			else:
				raise MyError('Cannot determine date range')
		if months is not None:
			endmonth = max(months)
		else:
			endmonth = 12
		if days is not None:
			endday = max(days)
		else:
			endday = LastDayOfMonth(endyear, endmonth)
			
		enddate = datetime.datetime.strptime(str(endyear)+"-"+str(endmonth)+"-"+str(endday), "%Y-%m-%d")
	
	if years is None:
		years = range(startyear, endyear+1)
	if months is None:
		months = range(1,13)
	if days is None:
		days = range(1,32)
	if hours is None:
		hours = range(0,24)
		
	datestmp = [ startdate + datetime.timedelta(days=d) for d in range( (enddate-startdate).days + 1) ]
	
	dates = [ [d.year,d.month,d.day] for d in datestmp if d.year in years and d.month in months and d.day in days]
		
	datehours = []
	for d in dates:
		for h in hours:
			datehours.append(d + [h])
			
	return [dates, datehours]