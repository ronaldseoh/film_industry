"""
########################################################################################
# umdb_mojoCharts.py: This modules provides functions for acquiring lists              #
# that contain the following info: (1) Names of top 150 Hollywood actors, producers,   #
# and directors by gross revenue. (2) Title of movies that are part of any franchises. #
########################################################################################
"""

import lxml.html
import umdb_http

def getTop100Actors():

	# All the names of the actors gather throughout this method
	# will be put into this list and be returned.
	actorsInTop100 = []
	
	# Get the first 50 people
	mojoTopActors50Page = umdb_http.getPage('http://www.boxofficemojo.com/people/?view=Actor&pagenum=1&sort=sumgross&order=DESC&&p=.htm')
	
	# If we can't get any response from the url above, return what we have so far (= empty).
	if mojoTopActors50Page == None:
		return actorsInTop100

	# Parse the response into tree
	mojoTopActors50Tree = lxml.html.parse(mojoTopActors50Page)
	
	# Get the rows of the tables that contains the names of actors
	# Get the iterator of the list and use next() to skip the first one since
	# that would be the header (not an actual actor).
	mojoTopActors50Iterator = iter(mojoTopActors50Tree.xpath('//table[contains(tr[1]/td[1]/font, "Row")]//tr'))
	next(mojoTopActors50Iterator) # Skip the header
	
	# Names are in the 2nd column of each row.
	for actor in mojoTopActors50Iterator:
		actorsInTop100.append(str.lower(actor.xpath('string(.//td[2])')))
	
	# Move on to other 50
	# At the moment, the page actually gives us names up to #150, not #100.
	# We just get 150 people because it doesn't really matter for our purpose.
	mojoTopActors100Page = umdb_http.getPage('http://www.boxofficemojo.com/people/?view=Actor&pagenum=2&sort=sumgross&order=DESC&&p=.htm')
	
	# If we can't get any response from the url above, return what we have so far (= first 50).
	if mojoTopActors100Page == None:
		return actorsInTop100
		
	# Parse the response into tree
	mojoTopActors100Tree = lxml.html.parse(mojoTopActors100Page)
	
	# Get the rows of the tables that contains the names of actors
	# Get the iterator of the list and use next() to skip the first one since
	# that would be the header (not actual actor).
	mojoTopActors100Iterator = iter(mojoTopActors100Tree.xpath('//table[contains(tr[1]/td[1]/font, "Row")]//tr'))
	next(mojoTopActors100Iterator)
	
	# Names are in the 2nd column of each row.
	for actor in mojoTopActors100Iterator:
		actorsInTop100.append(str.lower(actor.xpath('string(.//td[2])')))
	
	# Return the list	
	return actorsInTop100

def getTop100Producers():

	# All the names of the producers gather throughout this method
	# will be put into this list and be returned.
	producersInTop100 = []
	
	# Get the first 50 people
	mojoTopProducers50Page = umdb_http.getPage('http://www.boxofficemojo.com/people/?view=Producer&pagenum=1&sort=sumgross&order=DESC&&p=.htm')
	
	# If we can't get any response from the url above, return what we have so far (= empty).
	if mojoTopProducers50Page == None:
		return producersInTop100
	
	# Parse the response into tree
	mojoTopProducers50Tree = lxml.html.parse(mojoTopProducers50Page)
	
	# Get the rows of the tables that contains the names of actors
	# Get the iterator of the list and use next() to skip the first one since
	# that would be the header (not an actual producer).
	mojoTopProducers50Iterator = iter(mojoTopProducers50Tree.xpath('//table[contains(tr[1]/td[1]/font, "Row")]//tr'))
	next(mojoTopProducers50Iterator)
	
	# Names are in the 2nd column of each row.
	for producer in mojoTopProducers50Iterator:
		producersInTop100.append(str.lower(producer.xpath('string(.//td[2])')))
	
	# Move on to other 50
	# At the moment, the page actually gives us names up to #150, not #100.
	# We just get 150 people because it doesn't really matter for our purpose.
	mojoTopProducers100Page = umdb_http.getPage('http://www.boxofficemojo.com/people/?view=Producer&pagenum=2&sort=sumgross&order=DESC&&p=.htm')
	
	# If we can't get any response from the url above, return what we have so far (= first 50).
	if mojoTopProducers100Page == None:
		return producersInTop100	
	
	# Parse the response into tree
	mojoTopProducers100Tree = lxml.html.parse(mojoTopProducers100Page)
	
	# Get the rows of the tables that contains the names of actors
	# Get the iterator of the list and use next() to skip the first one since
	# that would be the header (not an actual producer).
	mojoTopProducers100Iterator = iter(mojoTopProducers100Tree.xpath('//table[contains(tr[1]/td[1]/font, "Row")]//tr'))
	next(mojoTopProducers100Iterator)
	
	# Names are in the 2nd column of each row.
	for producer in mojoTopProducers100Iterator:
		producersInTop100.append(str.lower(producer.xpath('string(.//td[2])')))
		
	return producersInTop100

def getTop100Directors():

	# All the names of the directors gather throughout this method
	# will be put into this list and be returned.
	directorsInTop100 = []
	
	mojoTopDirectors50Page = umdb_http.getPage('http://www.boxofficemojo.com/people/?view=Director&pagenum=1&sort=sumgross&order=DESC&&p=.htm')
	
	if mojoTopDirectors50Page == None:
		return directorsInTop100

	mojoTopDirectors50Tree = lxml.html.parse(mojoTopDirectors50Page)
	
	mojoTopDirectors50Iterator = iter(mojoTopDirectors50Tree.xpath('//table[contains(tr[1]/td[1]/font, "Row")]//tr'))
	next(mojoTopDirectors50Iterator) # Skip the header
	
	for director in mojoTopDirectors50Iterator:
		directorsInTop100.append(str.lower(director.xpath('string(.//td[2])')))
	
	mojoTopDirectors100Page = umdb_http.getPage('http://www.boxofficemojo.com/people/?view=Director&pagenum=2&sort=sumgross&order=DESC&&p=.htm')
	
	if mojoTopDirectors100Page == None:
		return directorsInTop100		
	
	mojoTopDirectors100Tree = lxml.html.parse(mojoTopDirectors100Page)
	
	mojoTopDirectors100Iterator = iter(mojoTopDirectors100Tree.xpath('//table[contains(tr[1]/td[1]/font, "Row")]//tr'))
	next(mojoTopDirectors100Iterator)
	
	for director in mojoTopDirectors100Iterator:
		directorsInTop100.append(str.lower(director.xpath('string(.//td[2])')))
		
	return directorsInTop100
		
def getFranchises():
	franchisesList = []
	
	mojoFranchisesPage = umdb_http.getPage('http://www.boxofficemojo.com/franchises/')
	
	if mojoFranchisesPage == None:
		return franchisesList
	
	mojoFranchisesTree = lxml.html.parse(mojoFranchisesPage)
	
	franchiseLinks = mojoFranchisesTree.xpath('//table[contains(tr[1]/td[1]/font/a/b/text(), "Franchise (click to view chart)")]//tr')
	franchiseLinks = iter(franchiseLinks)
	next(franchiseLinks)
	
	for franchise in franchiseLinks:
		franchise.make_links_absolute()
		franchiseHref = franchise.xpath('.//@href')[0]
		franchisesList = franchisesList + getFranchiseMovies(franchiseHref)
		
	return franchisesList

def getFranchiseMovies(franchiseHref):
	movieInFranchise = []
	
	mojoFranchisePage = umdb_http.getPage(franchiseHref)
	
	if mojoFranchisePage == None:
		return movieInFranchise
	
	mojoFranchiseTree = lxml.html.parse(mojoFranchisePage)
	
	# Exclude the last 2 rows of tables
	franchiseMovieList = mojoFranchiseTree.xpath('//table[contains(tr[1]/td[1]/font/a/text(), "Rank")]//tr')
	franchiseMovieList = franchiseMovieList[1:len(franchiseMovieList)-2]
	
	for movie in franchiseMovieList:
		movieInFranchise.append(str.lower(movie.xpath('string(.//td[2])')))

	return movieInFranchise