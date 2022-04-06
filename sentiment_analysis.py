import nltk
nltk.download('stopwords')
nltk.download('wordnet')

import pandas as pd 
from nltk.corpus import stopwords 
import math 
import statistics 
from sklearn.feature_extraction.text import CountVectorizer 
from textblob import TextBlob
from nltk.tokenize import TreebankWordTokenizer
from nltk.stem import WordNetLemmatizer
import pandas as pd
from transformers import pipeline

class SentimentAnalyser: 
    def __init__(self, dataframes): 
        for df in dataframes: 
            assert df.columns == ["model", "comments", "platform"]
        df_combined = pd.concat(dataframes)
        df_combined['cleaned_comments'] = df_combined['comments'].apply(lambda t: self.preprocess_text(t))
        self.df_combined = df_combined
        self.labels = {
            "zero_shot": "zero_shot", 
            "sentiment_analysis": "sentiment_analysis", 
        }

    def preprocess_text(self, text):
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
        
    def Textblob(self): 
        df = self.df_combined.copy() 
        df[self.labels['sentiments_analysis']] = df['comments'].apply(lambda text: TextBlob(text).sentiment.polarity)
        return df 

    def BERTSentimentAnalysis(self): 
        df = self.df_combined.copy() 
        classifier = pipeline("sentiment-analysis") 
        df[self.labels['sentiments_analysis']] = df['comments'].apply(lambda text: classifier(text)[0]['label'])
        return df 
        
    def ZeroShot(self, candidates=["sustainable", "unsustainable"]): 
        df = self.df_combined.copy() 
        classifier = pipeline("zero-shot-classification")
        df[self.labels['zero_shot']] = df['comments'].apply(lambda text: classifier(text, candidate_labels=candidates)[0]['label']) 
        return df

    def get_topwords(dataframesgroupby_model=True): 

        extra_stopwords = ["wa", "doe", "ha", "video", "one", "subscribe", "channel", "watch", "watching", "thanks", "thank"] 
        all_stopwords = stopwords.words('english')
        all_stopwords.extend(extra_stopwords) 

        return text 
    

if __name__ == '__main__':
    df = pd.read_pickle('combined_data.pkl')
    sentiment_analysis(df)
    df.to_csv('sentiment_analysis.csv')

