"""
###############################################################################
# film_industry_omdb.py: This modules gathers data from OMDb (http://www.omdbapi.com). #
###############################################################################
"""

import film_industry_http

def getOMDbJSONResponse(title, year):

	OMDbJSONUrl = 'http://www.omdbapi.com/?t=' + title + '&type=movie&y=' + year + '&plot=short&tomatoes=true'
	OMDbJSONUrl = OMDbJSONUrl.replace(' ', '%20')

	response = film_industry_http.getJSON(OMDbJSONUrl, 20)
	
	return response

def attemptDifferentVariations(title, year):

	data = getOMDbJSONResponse(title, year)
	
	# If 'response' is 'False', try looking at 
	# (1) one year before and after,
	# (2) title with ' and ' changed with ' & ', 
	# (3) and title with all the stuff in parentheses removed.
	try:
		if len(data) == 0 or data['Response'] == 'False':
			data = getOMDbJSONResponse(title, str(int(year)-1))
			if len(data) == 0 or data['Response'] == 'False':
				data = getOMDbJSONResponse(title, str(int(year)+1))
				if len(data) == 0 or data['Response'] == 'False':
					# Attempt modifying title
					revisedTitle = title.replace(' and ', ' & ', 1)
					if revisedTitle != title:
						data = attemptDifferentVariations(revisedTitle, year)
	except IndexError, KeyError:
		pass
		
	return data

def getOMDbData(title, year):

	OMDbOutput = {}
	
	OMDbJSONData = attemptDifferentVariations(title, year)
		
	try:
		OMDbOutput['metaScore'] = OMDbJSONData['Metascore']
	except:
		OMDbOutput['metaScore'] = '?'
		pass
	
	try:
		OMDbOutput['imdbRating'] = OMDbJSONData['imdbRating']
	except:
		OMDbOutput['imdbRating'] = '?'
		pass
		
	try:
		OMDbOutput['imdbVotes'] = OMDbJSONData['imdbVotes']
	except:
		OMDbOutput['imdbVotes'] = '?'
		pass
		
	try:
		OMDbOutput['tomatoMeter'] = OMDbJSONData['tomatoMeter']
	except:
		OMDbOutput['tomatoMeter'] = '?'
		pass
	
	try:
		OMDbOutput['tomatoImage'] = OMDbJSONData['tomatoImage']
	except:
		OMDbOutput['tomatoImage'] = '?'
		pass
	
	try:
		OMDbOutput['tomatoRating'] = OMDbJSONData['tomatoRating']
	except:
		OMDbOutput['tomatoRating'] = '?'
		pass
	
	try:
		OMDbOutput['tomatoReviews'] = OMDbJSONData['tomatoReviews']
	except:
		OMDbOutput['tomatoReviews'] = '?'
		pass
	
	try:
		OMDbOutput['tomatoFresh'] = OMDbJSONData['tomatoFresh']
	except:
		OMDbOutput['tomatoFresh'] = '?'
		pass
		
	try:
		OMDbOutput['tomatoRotten'] = OMDbJSONData['tomatoRotten']
	except:
		OMDbOutput['tomatoRotten'] = '?'
		pass
		
	try:
		OMDbOutput['tomatoUserMeter'] = OMDbJSONData['tomatoUserMeter']
	except:
		OMDbOutput['tomatoUserMeter'] = '?'
		pass
		
	try:
		OMDbOutput['tomatoUserRating'] = OMDbJSONData['tomatoUserRating']
	except:
		OMDbOutput['tomatoUserRating'] = '?'
		pass
		
	try:
		OMDbOutput['tomatoUserReviews'] = OMDbJSONData['tomatoUserReviews']
	except:
		OMDbOutput['tomatoUserReviews'] = '?'
		pass
	
	return OMDbOutput
	
