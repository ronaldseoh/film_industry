"""
########################################################
# umdb_main.py: Main execution script.                 #
########################################################
"""

import codecs
import umdb_mojo
import umdb_processing
import umdb_arff

# Fetch all the raw data
rawData = umdb_mojo.getAllMovieData()

# Process raw data suitable for arff
processedData = umdb_processing.doRefine(rawData)

# Write the processed data to new arff file
umdb_arff.writeARFFfile(processedData, codecs.open('ultimateMovieDB_beforeProcessing.arff','w', 'utf-8'))