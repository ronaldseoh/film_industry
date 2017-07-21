"""
########################################################
# film_industry_main.py: Main execution script.                 #
########################################################
"""

import codecs
import film_industry_mojo
import film_industry_processing
import film_industry_arff

# Fetch all the raw data
rawData = film_industry_mojo.getAllMovieData()

# Process raw data suitable for arff
processedData = film_industry_processing.doRefine(rawData)

# Write the processed data to new arff file
film_industry_arff.writeARFFfile(processedData, codecs.open('ultimateMovieDB_beforeProcessing.arff','w', 'utf-8'))