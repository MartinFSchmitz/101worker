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
        'creates': [['dump', 'featureLocation']]
    }
}

def update_file(context, f):
    try:
        # read the content of the file (primary resource)
        source = context.get_primary_resource(f)
        # tokenize the source file (stems without stopwords)
        sourceTokens = process_text(source)

        # read possible feature tokens
        featureTokens = get_feature_tokens()

        # calculate intersection between actual and possible tokens
        s_f_token_intersect = list(set(sourceTokens) & set(featureTokens))

        # read existing feature locations
        data = context.read_dump('featureLocation')

        # init data if empty
        if data is None:
            data = {}

        # get name of current contribution
        if f.startswith('contributions' + os.sep):
            contribution = f.split(os.sep)[1]
            
            # init new contribution if missing
            if data.get(contribution, None) is None:
                data[contribution] = []

            # calculate union of existing and new tokens
            data[contribution] = list(set(data[contribution]) | set(s_f_token_intersect))

        # save dump file
        context.write_dump('featureLocation', data)

    except UnicodeDecodeError:
        context.write_dump('featureLocation', {[]})
        print("Error occured while executing featureLocation for file " + f)


def run(context, change):
    # dispatch the modified file
    if change['type'] == 'NEW_FILE':
        update_file(context, change['file'])

    elif change['type'] == 'FILE_CHANGED':
        update_file(context, change['file'])

    else:
        update_file(context, change['file'])



def process_text(text):
    # stem and tokenize text
    remove_punctuation_map = dict((ord(char), None) for char in string.punctuation)
    text = text.lower().translate(remove_punctuation_map)
    tokens = nltk.word_tokenize(text)
    stemmer = PorterStemmer()
    tokens = remove_stopwords([stemmer.stem(t) for t in tokens])
    return tokens
 
def remove_stopwords(tokens):
    stopwords = nltk.corpus.stopwords.words('english')
    content = [w for w in tokens if w not in stopwords]
    return content

def get_feature_tokens():
    dir = os.path.dirname(__file__)
    with open(dir + os.sep + 'featureTokens.json') as data_file:    
        data = json.load(data_file)
    return data