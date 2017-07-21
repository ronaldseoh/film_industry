"""
###############################################################################
# film_industry_processing.py: This modules processes acquired data based on our needs #
# and converts them to format suitable for liac-arff module.                  #
###############################################################################
"""
import time
import re
import traceback
import film_industry_mojoCharts
import film_industry_settings

def doRefine(rawDataList):

	top100ActorsR = film_industry_mojoCharts.getTop100Actors()
	top100ProducersR = film_industry_mojoCharts.getTop100Producers()
	top100DirectorsR = film_industry_mojoCharts.getTop100Directors()
	franchisesR = film_industry_mojoCharts.getFranchises()

	newDataList = []

	for rawDataRow in rawDataList:

		try:
			newDataRow = []
			
			# Release Year: use this string later on the exact date
			try:
				processedTimeString = time.strptime(rawDataRow['releaseDate'], "%B %d, %Y")
				newDataRow.append(processedTimeString.tm_year)
			except:
				newDataRow.append('?')
			
			# title: just pass it on as string
			if len(rawDataRow['title']) == 0:
				newDataRow.append('?')
			else:
				newDataRow.append(rawDataRow['title'])
				
			# title - check franchise
			if rawDataRow['title'].lower() in franchisesR:
				newDataRow.append('true')
			else:
				newDataRow.append('false')

			# Distributor
			if len(rawDataRow['distributor']) == 0 or rawDataRow['distributor'].lower() == 'n/a' or rawDataRow['distributor'].lower() == 'na':
				newDataRow.append('?')
				newDataRow.append('?')
			else:
				newDataRow.append(rawDataRow['distributor'])
				if rawDataRow['distributor'] in film_industry_settings.majorDistributor:
					newDataRow.append('Major')
				elif rawDataRow['distributor'] in film_industry_settings.miniMajorDistributor:
					newDataRow.append('Mini-Major')
				else:
					newDataRow.append('Others')

			# Release Date
			newDataRow.append(str(processedTimeString.tm_mday) + '/' + str(processedTimeString.tm_mon) + '/' + str(processedTimeString.tm_year))
			# Check seasonality:
			# Christmas (November/December), Summer (May Through August), Easter (March and April), Other
			if 11 <= processedTimeString.tm_mon <= 12:
				newDataRow.append('Christmas')
			elif 5 <= processedTimeString.tm_mon <= 8:
				newDataRow.append('Summer')
			elif 3 <= processedTimeString.tm_mon <= 4:
				newDataRow.append('Easter')
			else:
				newDataRow.append('Other')

			# Genre: Just pass it on
			if len(rawDataRow['genre']) == 0 or rawDataRow['genre'].lower() == 'n/a' or rawDataRow['genre'].lower() == 'na':
				newDataRow.append('?')
			else:
				newDataRow.append(rawDataRow['genre'])

			# Budget
			if len(rawDataRow['budget']) == 0 or rawDataRow['budget'].lower() == 'n/a' or rawDataRow['budget'].lower() == 'na':
				newDataRow.append('?')
			else:
				budgetStringSplit = rawDataRow['budget'].split()
				if budgetStringSplit[-1].lower() == 'million':
					budgetAmountMillions = float(budgetStringSplit[-2].replace('$','',1))
					newDataRow.append(budgetAmountMillions * 1000000)
				else:
					budgetAmount = float(budgetStringSplit[0].replace(',','').replace('$','',1))
					newDataRow.append(budgetAmount)

			# Runtime
			if len(rawDataRow['runtime']) == 0 or rawDataRow['runtime'].lower() == 'n/a' or rawDataRow['runtime'].lower() == 'na':
				newDataRow.append('?')
			else:
				runtimeHours = 0
				runtimeMinutes = 0
				hoursMatch = re.search(r'(\d*[,]*)*\d+\s*hrs', rawDataRow['runtime'])
				if hoursMatch:
					runtimeHours = int(hoursMatch.group().split()[0])

				minutesMatch = re.search(r'(\d*[,]*)*\d+\s*min', rawDataRow['runtime'])
				if minutesMatch:
					runtimeMinutes = int(minutesMatch.group().split()[0])

				newDataRow.append(runtimeHours * 60 + runtimeMinutes)

			# Rating
			if len(rawDataRow['rating']) == 0 or rawDataRow['rating'].lower() == 'n/a' or rawDataRow['rating'].lower() == 'na':
				newDataRow.append('?')
			elif rawDataRow['rating'].lower() == 'unrated' or rawDataRow['rating'].lower() == 'not yet rated':
				newDataRow.append('Unrated')
			else: 
				newDataRow.append(rawDataRow['rating'])

			# US Domestic Gross
			try:
				newDataRow.append(float(rawDataRow['USGross'].replace(',','')))
			except:
				newDataRow.append('?')

			# Widest Releases
			try:
				newDataRow.append(int(rawDataRow['widestReleases'].replace(',','')))
			except:
				newDataRow.append('?')
				
			# Wide/Limited Release
			try:
				if int(rawDataRow['widestReleases'].replace(',','')) >= film_industry_settings.limitedCriteria:
					newDataRow.append('Wide')
				else:
					newDataRow.append('Limited')
			except:
				newDataRow.append('?')

			# Opening (Wide) Revenue
			try:
				newDataRow.append(float(rawDataRow['openingRevenue'].replace(',','')))
			except:
				newDataRow.append('?')
			
			# Opening (Wide) Rank
			try:
				newDataRow.append(int(rawDataRow['openingRank'].replace(',','')))
			except:
				newDataRow.append('?')

			# Opening (Wide) Theatre
			try:
				newDataRow.append(int(rawDataRow['openingTheater'].replace(',','')))
			except:
				newDataRow.append('?')

			# Opening (Wide) Average
			try:
				newDataRow.append(float(rawDataRow['openingAverage'].replace(',','')))
			except:
				newDataRow.append('?')
				
			# Number of Weeks
			try:
				newDataRow.append(int(rawDataRow['numberWeeks']))
			except:
				newDataRow.append('?')
				
			# 'Limited' Opening Weekend (Platform Release)
			newDataRow.append(rawDataRow['platform'])
			
			# Opening (Limited) Revenue
			try:
				newDataRow.append(float(rawDataRow['openingRevenueLimited'].replace(',','')))
			except:
				newDataRow.append('?')
			
			# Opening (Limited) Rank
			try:
				newDataRow.append(int(rawDataRow['openingRankLimited'].replace(',','')))
			except:
				newDataRow.append('?')

			# Opening (Limited) Theatre
			try:
				newDataRow.append(int(rawDataRow['openingTheaterLimited'].replace(',','')))
			except:
				newDataRow.append('?')

			# Opening (Limited) Average
			try:
				newDataRow.append(float(rawDataRow['openingAverageLimited'].replace(',','')))
			except:
				newDataRow.append('?')
				
			# Number of Weeks Limited
			try:
				newDataRow.append(int(rawDataRow['numberWeeksLimited']))
			except:
				newDataRow.append('?')
			
			# Director
			if len(rawDataRow['director']) == 0 or rawDataRow['director'].lower() == 'n/a' or rawDataRow['director'].lower() == 'na':
				newDataRow.append('?')
			elif rawDataRow['director'].lower() in top100DirectorsR:
				newDataRow.append('true')
			else:
				newDataRow.append('false')

			# Actors
			if len(rawDataRow['actors']) == 0:
				newDataRow.append('?')
				newDataRow.append('?')
			elif len(rawDataRow['actors']) >= 1:
				if rawDataRow['actors'][0].lower() in top100ActorsR:
					newDataRow.append('true')
				else:
					newDataRow.append('false')

				if len(rawDataRow['actors']) >= 2:
					if rawDataRow['actors'][1].lower() in top100ActorsR:
						newDataRow.append('true')
					else:
						newDataRow.append('false')
				else:
					newDataRow.append('false')

			# Producers
			if len(rawDataRow['producers']) == 0:
				newDataRow.append('?')
				newDataRow.append('?')
			elif len(rawDataRow['producers']) >= 1:
				if rawDataRow['producers'][0].lower() in top100ProducersR:
					newDataRow.append('true')
				else:
					newDataRow.append('false')

				if len(rawDataRow['producers']) >= 2:
					if rawDataRow['producers'][1].lower() in top100ProducersR:
						newDataRow.append('true')
					else:
						newDataRow.append('false')
				else:
					newDataRow.append('false')

			# Metascore
			if rawDataRow['metaScore'] == 'N/A':
				newDataRow.append('?')
			else:
				newDataRow.append(rawDataRow['metaScore'])

			# IMDb Rating
			if rawDataRow['imdbRating'] == 'N/A':
				newDataRow.append('?')
			else:
				newDataRow.append(rawDataRow['imdbRating'])

			# IMDb Votes
			if rawDataRow['imdbVotes'] == 'N/A':
				newDataRow.append('?')
			else:
				try:
					newDataRow.append(int(rawDataRow['imdbVotes'].replace(',','')))
				except:
					newDataRow.append('?')

			# Tomato Meter
			if rawDataRow['tomatoMeter'] == 'N/A':
				newDataRow.append('?')
			else:
				try:
					newDataRow.append(int(rawDataRow['tomatoMeter'].replace(',','')))
				except:
					newDataRow.append('?')				

			# Tomato Image
			if rawDataRow['tomatoImage'] == 'N/A':
				newDataRow.append('?')
			else:
				newDataRow.append(rawDataRow['tomatoImage'])

			# Tomato Rating
			if rawDataRow['tomatoRating'] == 'N/A':
				newDataRow.append('?')
			else:
				try:
					newDataRow.append(float(rawDataRow['tomatoRating'].replace(',','')))
				except:
					newDataRow.append('?')

			# Tomato Reviews
			if rawDataRow['tomatoReviews'] == 'N/A':
				newDataRow.append('?')
			else:
				try:
					newDataRow.append(int(rawDataRow['tomatoReviews'].replace(',','')))
				except:
					newDataRow.append('?')

			# Tomato Fresh
			if rawDataRow['tomatoFresh'] == 'N/A':
				newDataRow.append('?')
			else:
				try:
					newDataRow.append(int(rawDataRow['tomatoFresh'].replace(',','')))
				except:
					newDataRow.append('?')

			# Tomato Rotten
			if rawDataRow['tomatoRotten'] == 'N/A':
				newDataRow.append('?')
			else:
				try:
					newDataRow.append(int(rawDataRow['tomatoRotten'].replace(',','')))
				except:
					newDataRow.append('?')

			# Tomato User Meter
			if rawDataRow['tomatoUserMeter'] == 'N/A':
				newDataRow.append('?')
			else:
				try:
					newDataRow.append(int(rawDataRow['tomatoUserMeter'].replace(',','')))
				except:
					newDataRow.append('?')

			# Tomato User Rating
			if rawDataRow['tomatoUserRating'] == 'N/A':
				newDataRow.append('?')
			else:
				try:
					newDataRow.append(float(rawDataRow['tomatoUserRating'].replace(',','')))
				except:
					newDataRow.append('?')

			# Tomato User Reviews
			if rawDataRow['tomatoUserReviews'] == 'N/A':
				newDataRow.append('?')
			else:
				try:
					newDataRow.append(int(rawDataRow['tomatoUserReviews'].replace(',','')))
				except:
					newDataRow.append('?')
        
			newDataList.append(newDataRow)
			
		except Exception, e:
			print "Error occurred at row: " + str(rawDataList.Index(rawDataRow))
			traceback.print_exc()
			continue

	return newDataList
