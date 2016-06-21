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
					#print(type(newFeature))
					newFeature = newFeature.lower()
					newFeatureTokens = nltk.word_tokenize(newFeature)
					newFeatureTokensStem = [stemmer.stem(t) for t in newFeatureTokens]
					for tk in newFeatureTokensStem:
						wikiList [len(wikiList)-1].append(tk)
	# Now wikiList is a list with lists as elements.
	# Each of those list-elements contains the contribution name as first element
	# and the names of the features implemented in the contribution as elements.	
	#print(wikiList)
	#print("------------------")
	#print(realData)
	
	#ToDo: Stemming of the feature names in wikiList
	onlyWikiList = []
	onlyRealList = []
	#result = [['real','wiki']]
	for i in range(0,len(wikiList )):
	
		key = wikiList[i][0]
		wikiList[i].remove(key)
		#result.append(key)
		if key in realData:
			onlyWikiElement = list(set(wikiList[i]) - set(realData[key]))
			onlyRealElement = list(set(realData[key]) - set(wikiList[i]))
			onlyRealList.append(onlyRealElement)
			onlyWikiList.append(onlyWikiElement)
	print(onlyWikiList)
	print(onlyRealList)
