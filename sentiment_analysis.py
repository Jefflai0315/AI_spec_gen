import nltk
nltk.download('stopwords')
nltk.download('wordnet')

import pandas as pd 
from nltk.corpus import stopwords 
import math 
import statistics 
from sklearn.feature_extraction.text import CountVectorizer 
from nltk.tokenize import TreebankWordTokenizer
from nltk.stem import WordNetLemmatizer


def sentiment_analysis(dataframes): 
    # dataframes must have the colums model, comments, platform 
    for df in dataframes: 
        assert df.columns == ["model", "comments", "platform"]

    df_combined = pd.concat(dataframes)
    df_combined['cleaned_comments'] = df_combined['comments'].apply(lambda t: preprocess_text(t))


def preprocess_text(text):                               # user defined function for cleaning text
    text = text.lower()                             # all lower case
    text = re.sub(r'\[.*?\]', ' ', text)            # remove text within [ ] (' ' instead of '')
    text = re.sub(r'\<.*?\>', ' ', text)            # remove text within < > (' ' instead of '')
    text = re.sub(r'http\S+', ' ', text)            # remove website ref http
    text = re.sub(r'www\S+', ' ', text)             # remove website ref www

    text = text.replace('€', 'euros')               # replace special character with words
    text = text.replace('£', 'gbp')                 # replace special character with words
    text = text.replace('$', 'dollar')              # replace special character with words
    text = text.replace('%', 'percent')             # replace special character with words
    text = text.replace('\n', ' ')                  # remove \n in text that has it

    text = text.replace('\'', '’')                  # standardise apostrophe
    text = text.replace('&#39;', '’')               # standardise apostrophe

    text = text.replace('’d', ' would')             # remove ’ (for would, should? could? had + PP?)
    text = text.replace('’s', ' is')                # remove ’ (for is, John's + N?)
    text = text.replace('’re', ' are')              # remove ’ (for are)
    text = text.replace('’ll', ' will')             # remove ’ (for will)
    text = text.replace('’ve', ' have')             # remove ’ (for have)
    text = text.replace('’m', ' am')                # remove ’ (for am)
    text = text.replace('can’t', 'can not')         # remove ’ (for can't)
    text = text.replace('won’t', 'will not')        # remove ’ (for won't)
    text = text.replace('n’t', ' not')              # remove ’ (for don't, doesn't)

    text = text.replace('’', ' ')                   # remove apostrophe (in general)
    text = text.replace('&quot;', ' ')              # remove quotation sign (in general)

    text = text.replace('cant', 'can not')          # typo 'can't' (note that cant is a proper word)
    text = text.replace('dont', 'do not')           # typo 'don't'

    text = re.sub(r'[^a-zA-Z0-9]', r' ', text)      # only alphanumeric left
    text = text.replace("   ", ' ')                 # remove triple empty space
    text = text.replace("  ", ' ')                  # remove double empty space

    tokens = TreebankWordTokenizer().tokenize(text)
    tokens = list(map(WordNetLemmatizer().lemmatize, tokens))
    preprocessed_text = " ".join(tokens)

    return preprocessed_text

def clean_comments(text): 

    extra_stopwords = ["wa", "doe", "ha", "video", "one", "subscribe", "channel", "watch", "watching", "thanks", "thank"] 
    all_stopwords = stopwords.words('english')
    all_stopwords.extend(extra_stopwords) 

    return text 


