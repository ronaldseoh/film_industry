"""
###############################################################################
# film_industry_http.py: This modules processes HTTP requests needed by other modules. #
###############################################################################
"""
import urllib2
import time
import json

def getPage(url, waitTime=10):
	requestedHTTPPage = None
	
	for _ in range(3):
		try:
			requestedHTTPPage = urllib2.urlopen(url)
			break
		except:
			time.sleep(waitTime)
			pass
			
	return requestedHTTPPage

def getJSON(url, waitTime):

	jsonData = {}
	
	jsonResponse = getPage(url, waitTime)
	
	try:
		jsonData = json.load(jsonResponse)
	except:
		pass

	return jsonData