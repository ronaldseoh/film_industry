"""
###########################################################################
# film_industry_arff.py: This module gets the processed data as                    #
# input and writes them as arff file, along with header information.      #
# Please refer to http://weka.wikispaces.com/ARFF+%28developer+version%29 # 
# for more detailed description of arff format.							  #
# Also, this module uses liac-arff package for actual writing to ARFF.    #
# Please refer to https://pythonhosted.org/liac-arff/ for details.	      #
###########################################################################
"""

import arff
import film_industry_settings

def writeARFFfile(dataList, fileObject):

	# Get attribute declarations
	attributeList = film_industry_settings.attributeList
	
	# Add class variable if needed - please uncomment corresponding sections
	# from other modules as well.
	# classificationTarget = film_industry_settings.classificationTarget
	# attributeList.append(('class', classificationTarget))

	# arff.dump takes a dictionary as an input
	dataARFFdict = {}

	# relation declaration
	dataARFFdict['relation'] = film_industry_settings.relation
	# attribute declaration
	dataARFFdict['attributes'] = attributeList
	# data declaration
	dataARFFdict['data'] = dataList

	# Write to the final arff file
	# codecs package is being used here along with utf-8 encoding
	# because dataList might contain unicode strings.
	arff.dump(dataARFFdict, fileObject)
