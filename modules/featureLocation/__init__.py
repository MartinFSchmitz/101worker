import os
import json
import nltk
import string
from nltk.stem.porter import PorterStemmer
from nltk.corpus import stopwords

config = {
    'wantdiff': True,
    'wantsfiles': True,
    'threadsafe': True,
    'behavior': {
        'creates': [['resource', 'fl']]
    }
}

# this is the actual logic of the module

def update_file(context, f):
    # reads the content of the file (primary resource)
    try:
        source = context.get_primary_resource(f)
        tokens = remove_stopwords(process_text(source))

        context.write_derived_resource(f, tokens, 'fl')
    except UnicodeDecodeError:
        context.write_derived_resource(f, 0, 'fl')

def remove_file(context, f):
    context.remove_derived_resource(f, 'fl')

def run(context, change):
    # dispatch the modified file
    if change['type'] == 'NEW_FILE':
        update_file(context, change['file'])

    elif change['type'] == 'FILE_CHANGED':
        update_file(context, change['file'])

    else:
        remove_file(context, change['file'])

remove_punctuation_map = dict((ord(char), None) for char in string.punctuation)

def process_text(text):
    text = text.lower().translate(remove_punctuation_map)
    tokens = nltk.word_tokenize(text)
    stemmer = PorterStemmer()
    tokens = [stemmer.stem(t) for t in tokens]
    return tokens
 
def remove_stopwords(tokens):
    stopwords = nltk.corpus.stopwords.words('english')
    content = [w for w in tokens if w not in stopwords]
    return content

