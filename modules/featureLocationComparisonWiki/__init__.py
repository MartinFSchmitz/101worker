import os
import json
import nltk
import string
from nltk.stem.porter import PorterStemmer
from nltk.corpus import stopwords

config = {
	'wantdiff': False,
	'wantsfiles': False,
	'threadsafe': True,
	'behavior': {
		'creates': [['dump', 'featureLocationComparisonWiki']]
	}
}
def run(context):
	# reads Data from Wiki and from the Contributions
	realData = context.read_dump('featureLocation')
	wikiData = context.read_dump('wiki-links') ['wiki'] ['pages']
	
	#Runs through all Wiki Pages searching for features in every contribution
	stemmer = PorterStemmer()
	wikiList = []
	for i in range(1,len(wikiData )):
		if 'Implements' in wikiData [i]:
			contribution = wikiData [i] ['n']
			wikiList.append([contribution])
			for j in range(0,len(wikiData [i] ['Implements'])):
				
				if wikiData [i] ['Implements'] [j] ['p'] == 'Feature':
					newFeature = wikiData [i] ['Implements'] [j] ['n']
					#Stemming and adding to list
					wikiList [len(wikiList)-1].append(stemmer.stem(newFeature.lower()))
	# Now wikiList is a list with lists as elements.
	# Each of those list-elements contains the contribution name as first element
	# and the names of the features implemented in the contribution as elements.	
	#print(wikiList)
	#print("------------------")
	#print(realData)
	
	#ToDo: Stemming of the feature names in wikiList
	#stemmer = PorterStemmer()
	#for i in range(0, len(wikiList)):
	#	for j in range(0, len(wikiList[i])):
	#		text = wikiList[i][j].lower()
	#		token = stemmer.stem(text)
	#		print(token)

	#compare wikilist with realData
	for i in range(0, len(wikiList)):
		search = wikiList[i] [0]
		if search in realData:
			print(search + ":")
			for j in range(0, len(realData[search])):
				print(realData[search] [j])
