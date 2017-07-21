"""
##################################################################
# umdb_settings.py: This module contains variables with various  # 
# criteria or settings needed for crawling and processing.       #
# Please modify based on your needs.                             #
##################################################################
"""

# Search conditions
yearStart = 2006
yearEnd = 2013
majorDistributor = ['Warner Bros.','Buena Vista','Sony / Columbia', 'Sony / Screen Gems', 'Paramount','20th Century Fox','Universal','New Line','Miramax','Fox Searchlight','Focus Features','Sony Classics','Paramount Vantage','Warner Independent','Fox','Warner Bros. (New Line)','Fox Atomic','Sony (Revolution)','Paramount Classics','Paramount (DreamWorks)','TriStar','Columbia','Sony Pictures Home Ent.']
miniMajorDistributor = ['MGM/UA','United Artists','Lionsgate','Lions Gate','DreamWorks SKG','Orion','Weinstein Company','Summit Entertainment','Dimension Films','Relativity','Open Road Films','AMC Theaters','FilmDistrict','IFC','Samuel Goldwyn','Overture Films','CBS Films','Rogue Pictures','Roadside Attractions','Radius-TWC','Lionsgate/Summit','Weinstein / Dimension','Weinstein / Dragon Dynasty','MGM (Weinstein)','MGM']
limitedCriteria = 600

# ARFF settings
relation = 'ultimateMovieDB'
attributeList = [('year', []),
('title','STRING'),
('franchise',['true','false']),
('distributor','STRING'),
('major',['Major','Mini-Major','Others']),
('release date','STRING'),
('seasonality',['Christmas','Summer','Easter','Other']),
('genre','STRING'),
('budget','NUMERIC'),
('runtime','NUMERIC'),
('rating', ['G','PG','PG-13','R','NC-17','Unrated']),
('US Gross','NUMERIC'),
('widest release', 'NUMERIC'),
('limited release', ['Wide', 'Limited']),
('opening revenue', 'NUMERIC'),
('opening rank', 'NUMERIC'),
('opening theaters', 'NUMERIC'),
('opening average', 'NUMERIC'),
('number of weeks', 'NUMERIC'),
('platform', ['true','false']),
('limited opening revenue', 'NUMERIC'),
('limited opening rank', 'NUMERIC'),
('limited opening theaters', 'NUMERIC'),
('limited opening average', 'NUMERIC'),
('limited number of weeks', 'NUMERIC'),
('director',['true','false']),
('actor1',['true','false']),
('actor2',['true','false']),
('producer1',['true','false']),
('producer2',['true','false']),
('metascore','NUMERIC'),
('imdb rating', 'NUMERIC'),
('imdb votes', 'NUMERIC'),
('tomato meter', 'NUMERIC'),
('tomato image',['rotten','fresh','certified']),
('tomato rating', 'NUMERIC'),
('tomato reviews', 'NUMERIC'),
('tomato fresh', 'NUMERIC'),
('tomato rotten', 'NUMERIC'),
('tomato user meter', 'NUMERIC'),
('tomato user rating', 'NUMERIC'),
('tomato user reviews', 'NUMERIC')]

# Please uncomment the following if you need class variable.
# classificationTarget = ['high','mid','low']

# Based on the yearStart and yearEnd values listed above, the following loop
# generates possible values for WEKA nominal variable 'year'.
yearAttributeList = []

for x in range(yearStart, yearEnd + 1):
	yearAttributeList.append(str(x))

attributeList[0] = ('year', yearAttributeList)