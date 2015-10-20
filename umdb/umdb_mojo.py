"""
################################################################################################
# umdb_mojo.py: This module acquires data from Box Office Mojo (http://www.boxofficemojo.com), #
# our primary dataset for the project.			         									   #
################################################################################################
"""

import umdb_settings
import umdb_omdb
import umdb_http
import lxml.html
import re
import time
import datetime

def getAllMovieData():

	yearStart = umdb_settings.yearStart
	yearEnd = umdb_settings.yearEnd
	
	allMovieDataList = []
	
	mojoIndexPage = umdb_http.getPage('http://www.boxofficemojo.com/movies/')

	if mojoIndexPage == None:
		return allMovieDataList

	mojoIndexTree = lxml.html.parse(mojoIndexPage)

	# Get list of links to alphabets
	alphabetLinksTable = mojoIndexTree.xpath('//tr[starts-with(td[1]/font/b/a/text(), "#")]')
	alphabetLinks = alphabetLinksTable[0].xpath('.//td//a')
	
	alphabetSubLinksList = []
	
	for alpha in alphabetLinks:
		alpha.make_links_absolute()
		mojoAlphabetPage = umdb_http.getPage(alpha.xpath('.//@href')[0])
		
		if mojoAlphabetPage == None:
			break
		
		mojoAlphabetTree = lxml.html.parse(mojoAlphabetPage)
		# Deal with subpages
		alphaSubPageCount = len(mojoAlphabetTree.xpath('//div[@id = \'body\']//div[@class = \'alpha-nav-holder\'][1]/font//b'))
		
		for i in range(alphaSubPageCount):
			alphabetSubLinksList.append(alpha.xpath('.//@href')[0] + '&page=' + str(i+1))

	for alphaHref in alphabetSubLinksList:
		allMovieDataList = allMovieDataList + processMojoAlphabet(alphaHref, yearStart, yearEnd)
		
	# Show the total number of movies fetched
	print ('Total number of movies fetched: ' + str(len(allMovieDataList)))
	
	return allMovieDataList
	
def processMojoAlphabet(alphabetLink, yearStart, yearEnd):

	movieDataList = []
	
	mojoAlphabetPage = umdb_http.getPage(alphabetLink)

	if mojoAlphabetPage == None:
		return None

	mojoAlphabetTree = lxml.html.parse(mojoAlphabetPage)

	mojoAlphabetMovieTable = mojoAlphabetTree.xpath('//table[contains(tr[1]/td[1]/font, "Title (click to view box office)")]//tr')
	
	for movieRow in mojoAlphabetMovieTable:
	
		if len(movieRow) < 7:
			continue

		# The page lists release dates on 7th column of the table. We try to check 
		# this value and skip the movie if it falls outside our search range.
		try:
			timeMovie = movieRow.xpath('./td[7]/font/a')
			if len(timeMovie) == 0:
				timeMovieString = movieRow.xpath('./td[7]/font')[0].text
			else:
				timeMovieString = timeMovie[0].text
			
			timeMovieRelease = time.strptime(timeMovieString, "%m/%d/%Y")
		except ValueError:
			continue
		except IndexError:
			continue
		
		# Check the release date column and ignore ones that fall outside our year range
		if timeMovieRelease.tm_year < yearStart:
			continue
			
		if timeMovieRelease.tm_year > yearEnd:
			continue
			
		movieLinkTag = movieRow.xpath('./td[1]/font/a')[0]
		movieLinkTag.make_links_absolute()
		movieLink = movieLinkTag.xpath('./@href')[0]
		
		movieLinkInfo = processMojoMovie(movieLink)
		
		if movieLinkInfo == None:
			continue
		else:
			movieDataList.append(movieLinkInfo)
		
	return movieDataList

def processMojoMovie(movieLink):

	movieValue = {}
	
	mojoMoviePage = umdb_http.getPage(movieLink)

	if mojoMoviePage == None:
		return None
	
	mojoMovieTree = lxml.html.parse(mojoMoviePage)
	
	# Get title
	titleString = mojoMovieTree.xpath('string(/html/head/title)')
	titleString = re.sub(r'\s*\([0-9]{1,4}\)\s*-\s*Box\s*Office\s*Mojo', '', titleString)
	
	titleOMDbSearchString = re.sub(r'\s*\([0-9]{1,4}\)', '', titleString) # this is just for OMDb search
	movieValue['title'] = titleString
	
	# Get distributor, release date, genre, runtime, rating, and budget from the upper table
	# Distributor
	distributorString = mojoMovieTree.xpath('string(//tr[starts-with(td[1], "Distributor: ")]/td[1])').replace('Distributor: ', '', 1)
	movieValue['distributor'] = distributorString
	
	# Release Date
	releaseDateString = mojoMovieTree.xpath('string(//tr[starts-with(td[2], "Release Date: ")]/td[2])').replace('Release Date: ', '', 1)
	yearOMDbSearchString = releaseDateString.split()[-1]
	movieValue['releaseDate'] = releaseDateString
	
	# Genre
	genreString = mojoMovieTree.xpath('string(//tr[starts-with(td[1], "Genre: ")]/td[1])').replace('Genre: ', '', 1)
	movieValue['genre'] = genreString
	
	# Budget
	budgetString = mojoMovieTree.xpath('string(//tr[starts-with(td[2], "Production Budget: ")]/td[2])').replace('Production Budget: ', '', 1)
	movieValue['budget'] = budgetString
	
	# Runtime
	runtimeString = mojoMovieTree.xpath('string(//tr[starts-with(td[2], "Runtime: ")]/td[2])').replace('Runtime: ', '', 1)
	movieValue['runtime'] = runtimeString
	
	# Rating
	ratingString = mojoMovieTree.xpath('string(//tr[starts-with(td[1], "MPAA Rating: ")]/td[1]/b)')
	movieValue['rating'] = ratingString
	
	# Get US gross revenue, widest release, opening weekend data from the summary page below
	
	# US Gross Revenue
	USGrossString = mojoMovieTree.xpath('string(//tr[starts-with(td[1], "Domestic:")]/td[2])').replace(u'\xa0', '', 1).replace(u'$', '', 1)
	movieValue['USGross'] = USGrossString
	
	# Widest Releases
	widestReleasesString = mojoMovieTree.xpath('string(//tr[starts-with(td[1], "Widest' + u'\xa0' +'Release:")]/td[2])').replace(u'\xa0','',1).replace(' theaters', '', 1)
	movieValue['widestReleases'] = widestReleasesString

	# Opening Weekend values

	# Revenue
	revenueOpeningString = mojoMovieTree.xpath('string(//tr[starts-with(td[1], "Wide' + u'\xa0' + 'Opening' + u'\xa0' + 'Weekend:")]/td[2])').replace(u'\xa0', '', 1).replace(u'$', '', 1)
	
	# If there's no separate 'Wide Opening Weekend' section, go for just 'Opening Weekend'
	if len(revenueOpeningString) == 0:
		# Opening Weekend Revenue
		revenueOpeningString = mojoMovieTree.xpath('string(//tr[starts-with(td[1], "Opening' + u'\xa0' + 'Weekend:")]/td[2])').replace(u'\xa0', '', 1).replace(u'$', '', 1)
		# Get opening weekend information that are written right below opening weekend revenues
		openingWeekendInfo = mojoMovieTree.xpath('string(//tr[starts-with(td[1], "Opening' + u'\xa0' + 'Weekend:")]/following-sibling::tr/td[1])').replace('(','',1).replace(')','',1)
		
		# Since there was no separate 'wide opening', this movie is not 'platform release'
		movieValue['platform'] = 'false'
		
	else:
		# Get opening weekend information that are written right below opening weekend revenues (wide)
		openingWeekendInfo = mojoMovieTree.xpath('string(//tr[starts-with(td[1], "Wide' + u'\xa0' + 'Opening' + u'\xa0' + 'Weekend:")]/following-sibling::tr/td[1])').replace('(','',1).replace(')','',1)
		
		# If there is a 'Wide Opening Weekend' section, that movie must have had a 'platform release', meaning
		# it had a limited release before its wide release.
		# Then check for 'Limited Opening Weekend' as well, and record the values recorded for that section as well. 
		
		# Get Opening Revenue and Info for 'Limited Opening Weekend'
		revenueOpeningLimitedString = mojoMovieTree.xpath('string(//tr[starts-with(td[1], "Limited' + u'\xa0' + 'Opening' + u'\xa0' + 'Weekend:")]/td[2])').replace(u'\xa0', '', 1).replace(u'$', '', 1)
		openingWeekendLimitedInfo = mojoMovieTree.xpath('string(//tr[starts-with(td[1], "Limited' + u'\xa0' + 'Opening' + u'\xa0' + 'Weekend:")]/following-sibling::tr/td[1])').replace('(','',1).replace(')','',1)
		
		# Since there is separate 'wide opening', this movie IS 'platform release'
		movieValue['platform'] = 'true'

	# Record Opening Weekend Revenue (Wide)
	movieValue['openingRevenue'] = revenueOpeningString
	
	# Parse Opening Weekend Info String (Wide)
	# Opening Weekend Ranking (Wide)
	openingWeekendRank = re.search(r'#(\d*[,]*)*\d+\s*rank', openingWeekendInfo)
	if openingWeekendRank:
		movieValue['openingRank'] = openingWeekendRank.group().replace('#','',1).replace(' rank', '', 1)
	else:
		movieValue['openingRank'] =  ''
		
	# Opening Weekend Theaters (Wide)
	openingWeekendTheater = re.search(r'(\d*[,]*)*\d+\s*theaters', openingWeekendInfo)
	if openingWeekendTheater:
		movieValue['openingTheater'] = openingWeekendTheater.group().replace(' theaters', '', 1)
	else:
		movieValue['openingTheater'] = ''
		
	# Opening Average (Wide)
	openingWeekendAverage = re.search(r'\$(\d*[,]*)*\d+\s*average', openingWeekendInfo)
	if openingWeekendAverage:
		movieValue['openingAverage'] = openingWeekendAverage.group().replace('$', '', 1).replace(' average', '', 1)
	else:
		movieValue['openingAverage'] = ''
	
	# Parse 'Limited' Opening Weekend Info (if they exist)
	if movieValue['platform'] == 'true':
	
		# Record Opening Weekend Revenue (Limited)
		movieValue['openingRevenueLimited'] = revenueOpeningLimitedString
		
		# Opening Weekend Ranking (Limited)
		openingWeekendRankLimited = re.search(r'#(\d*[,]*)*\d+\s*rank', openingWeekendLimitedInfo)
		if openingWeekendRankLimited:
			movieValue['openingRankLimited'] = openingWeekendRankLimited.group().replace('#','',1).replace(' rank', '', 1)
		else:
			movieValue['openingRankLimited'] = ''
			
		# Opening Weekend Theaters (Limited)
		openingWeekendTheaterLimited = re.search(r'(\d*[,]*)*\d+\s*theaters', openingWeekendLimitedInfo)
		if openingWeekendTheaterLimited:
			movieValue['openingTheaterLimited'] = openingWeekendTheaterLimited.group().replace(' theaters', '', 1)
		else:
			movieValue['openingTheaterLimited'] = ''
			
		# Opening Average (Limited)
		openingWeekendAverageLimited = re.search(r'\$(\d*[,]*)*\d+\s*average', openingWeekendLimitedInfo)
		if openingWeekendAverageLimited:
			movieValue['openingAverageLimited'] = openingWeekendAverageLimited.group().replace('$', '', 1).replace(' average', '', 1)
		else:
			movieValue['openingAverageLimited'] = ''
			
	else: # Since 'platform' is 'false', there is no 'limited opening weekend' section.
		movieValue['openingRevenueLimited'] = ''
		movieValue['openingRankLimited'] = ''
		movieValue['openingTheaterLimited'] = ''
		movieValue['openingAverageLimited'] = ''
	
	# Get Number of Weeks
	numberWeeksString = mojoMovieTree.xpath('//tr[starts-with(td[1]/font/a/b, "> View All")]/td[1]/font/a/b/text()')
	if len(numberWeeksString) == 0:
		movieValue['numberWeeks'] = ''
	else:
		for match in numberWeeksString:
			# On each movie page, there is a link that says '> View All (number) Weekends'.
			# We are trying to extract that number, which is a number of weeks for each movie.
			if match.find('Weekends') != -1:
				numberWeeksSearch = re.search(r'(\d*[,]*)*\d+\s*Weekends', match)
				
				# In some movies, the text is just '> View All Weekends' (no number between 'All' and 'Weekends'),
				# which means the movie was released for just 2 weeks (or less). 
				if not numberWeeksSearch:
					movieValue['numberWeeks'] = 2
				else:
					movieValue['numberWeeks'] = numberWeeksSearch.group().replace(' Weekends', '', 1)

				break

	# If the movie had a platform release, get the number of weeks under platform release as well.
	try:
		if movieValue['platform'] == 'true':
			numberWeeksLimitedString = mojoMovieTree.xpath('//tr[starts-with(td[1], "Release' + u'\xa0' + 'Dates:")]/td[2]/b/a/text()')
			limitedReleaseDate = datetime.datetime.strptime(numberWeeksLimitedString[0], "%B %d, %Y")
			wideReleaseDate = datetime.datetime.strptime(numberWeeksLimitedString[1], "%B %d, %Y")
			numberDaysLimitedWide = (wideReleaseDate - limitedReleaseDate).days
		
			movieValue['numberWeeksLimited'] = numberDaysLimitedWide / 7
		else:
			movieValue['numberWeeksLimited'] = ''
	except NameError, IndexError:
		movieValue['numberWeeksLimited'] = ''
	
	# Get director, actor, producer info from the table on the right
	directorString = mojoMovieTree.xpath('string(//tr[starts-with(td[1], "Director:")]/td[2])')
	movieValue['director'] = directorString
	
	actorsStringList = mojoMovieTree.xpath('//tr[starts-with(td[1], "Actors:")]/td[2]//a/text()')
	movieValue['actors'] = actorsStringList

	producersStringList = mojoMovieTree.xpath('//tr[starts-with(td[1], "Producers:")]/td[2]//a/text()')
	movieValue['producers'] = producersStringList
	
	# Get other data about this movie from OMDb and combine them with existing data (dictionary)
	OMDbData = umdb_omdb.getOMDbData(titleOMDbSearchString, yearOMDbSearchString)
	movieValue.update(OMDbData)
		
	# Print extracted data for each movie
	print(movieValue)
	
	# Make a delay between each movie pages
	time.sleep(3)
	
	if len(movieValue) == 0:
		return None
	else:
		return movieValue