'''A py file to build pipeline for preprocessing'''

"""
Some of the common text preprocessing / cleaning steps are:
- Tokenization: v
- Lower casing: v
- Removal of Numbers: v
- Removal of Punctuations:  v
- Removal of Stopwords: v
- Lemmatization: v

"""
import pandas as pd
import warnings
warnings.filterwarnings("ignore")
import string
from nltk.corpus import stopwords
# from spellchecker import Spellchecker
from nltk.tokenize import word_tokenize
import nltk
nltk.download('punkt')
nltk.download('wordnet')
from nltk.stem.porter import PorterStemmer
from nltk.stem import WordNetLemmatizer
import spacy


nlp = spacy.load('en_core_web_md', disable=['parser', 'ner'])

def lemmatization(texts,allowed_postags=['NOUN', 'ADJ']): 
      output = []
      for sent in texts:
            doc = nlp(sent) 
            output.append([token.lemma_ for token in doc if token.pos_ in allowed_postags ])
      return output


def preprocess_data(data):
    data = data.drop_duplicates(subset = 'Text')
    # Choose text >= 20
    data['Num_words_text'] = data['Text'].apply(lambda x:len(str(x).split())) 
    df_filtered_reviews = data[(data['Num_words_text'] >=20)]

    # Balacing the review
    df_sampled = df_filtered_reviews.groupby('Score').apply(lambda x: x.sample(n=10000, random_state = 17)).reset_index(drop = True)
    return df_sampled


def preprocess_text(text):
    '''Taking only Nouns from reviews'''
    # Lowercasing
    text = text.lower()
    
    # Removing punctuation
    text = text.translate(str.maketrans('', '', string.punctuation))
    
    # Removing numbers
    text = ' '.join(w for w in text.split() if ( not w.isdigit() and  ( not w.isdigit() and len(w)>3)))

    # Removing stopwords
    stop_words = set(stopwords.words('english'))
    custom_stopwords = ['i\'m', 'i\'ll']
    stop_words.update(custom_stopwords)
    text = " ".join([word for word in text.split() if word not in stop_words])


    # Lemmatizing only nouns
    lemmatized_tokens = lemmatization([text], allowed_postags=['NOUN'])
    text = " ".join(lemmatized_tokens[0])
    
    # Tokenizing
    tokens = word_tokenize(text)
    
    return tokens