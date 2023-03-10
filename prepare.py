# unicode, regex, json for text digestion
import unicodedata
import re
import json

# nltk: natural language toolkit -> tokenization, stopwords
import nltk
from nltk.tokenize.toktok import ToktokTokenizer
from nltk.corpus import stopwords

# pandas dataframe manipulation, acquire script, time formatting
import pandas as pd
import acquire
from time import strftime


def basic_clean(string):
    '''
    Description:
    This function takes in the string argument and returns the string normalized, cleaned, and lowercase.
    
    Required Imports:
    import re
    
    Arguments:
    string = The string of text to be cleaned
    
    Returns:
    string - After being cleaned
    '''
    string = unicodedata.normalize('NFKD', string)\
             .encode('ascii', 'ignore')\
             .decode('utf-8', 'ignore')
    string = re.sub(r"[^\w0-9'\s]", '', string).lower()
    return string

def tokenize(string):
    '''
    Description:
    This function takes in the string argument and returns the string tokenized.
    
    Required Imports:
    import nltk
    from nltk.tokenize.toktok import ToktokTokenizer
    
    Arguments:
    string = The string of text to be cleaned
    
    Returns:
    string - After being cleaned
    '''
    tokenizer = nltk.tokenize.ToktokTokenizer()
    string = tokenizer.tokenize(string, return_str = True)
    
    return string

def stem(string):
    '''
    Description:
    This function takes in the string argument and returns the stemmed words.
    
    Required Imports:
    import nltk
    
    Arguments:
    string = The string of text to be cleaned
    
    Returns:
    string - After being cleaned    
    '''
    ps = nltk.porter.PorterStemmer()
    stems = [ps.stem(word) for word in string.split()]
    string = ' '.join(stems)
    
    return string

def lemmatize(string):
    '''
    Description:
    This function takes in the string argument and returns a string with words lemmatized.
    
    Required Imports:
    import nltk
    
    Arguments:
    string = The string of text to be cleaned
    
    Returns:
    string - After being cleaned    
    '''
    wnl = nltk.stem.WordNetLemmatizer()
    lemmas = [wnl.lemmatize(word) for word in string.split()]
    string = ' '.join(lemmas)
    return string

def remove_stopwords(string, extra_words = [], exclude_words = []):
    '''
    Description:
    This function takes in a string, optional extra_words and exclude_words parameters
    with default empty lists and returns a string.
    
    Required Imports:
    import nltk
    from nltk.corpus import stopwords
    
    Arguments:
           string = The string of text to be cleaned
      extra_words = Holds List of words to be added to the stopwords list 
    exclude_words = Holds List of words to be removed from the stopwords list 
    
    Returns:
    string - After being cleaned    
    '''
    stopword_list = stopwords.words('english')
    stopword_list = set(stopword_list) - set(exclude_words)
    stopword_list = stopword_list.union(set(extra_words))
    words = string.split()
    filtered_words = [word for word in words if word not in stopword_list]
    string = ' '.join(filtered_words)
    return string

def prep_article_data(df, column_name, extra_words=[], exclude_words=[]):
    '''
    Description:
    This function takes in a df and the string name for a text column with 
    option to pass lists for extra_words and exclude_words and
    returns a df with the text article title, original, cleaned, tokenized, & lemmatized text.
        
    Required Imports:
    import nltk
    import pandas as pd
    
    Arguments:
               df = DataFrame
      column_name = The name of the 'column' that holds the target text to be prepared.
      extra_words = Holds List of words to be added to the stopwords list 
    exclude_words = Holds List of words to be removed from the stopwords list 
        
    Returns:
    df - DataFrame with each of the columns: 'title', 'original', 'clean', 'stemmed', 'lemmatized'    
    '''
    df['clean'] = df[column_name].apply(basic_clean)\
                            .apply(tokenize)\
                            .apply(remove_stopwords,
                                  extra_words=extra_words,
                                  exclude_words=exclude_words)
    
    df['original'] = df[column_name] 
    
    df['stemmed'] = df['clean'].apply(stem)
    
    df['lemmatized'] = df['clean'].apply(lemmatize)
    
    return df[['title', 'original', 'clean', 'stemmed', 'lemmatized']]

def clean(text, stem_or_lem=None, add_stopwords=[]):
    """
    Description:
    Simplified text cleaning function
    
    Required Imports:
    import re
    import nltk
    import unicodedata
    import pandas as pd
    from nltk.corpus import stopwords

    Arguments:
             text = The text you want to clean
      stem_or_lem = Default is None; stem will perform stemming on your text; lem will lemmatize it.
    add_stopwords = [] This is an empty list by default; just add words that you want to include as stopwords.
    
    Returns:
    returns list of cleaned words.
    """
    # 1. lowercase everything
    text = text.lower()
    # 2. Remove accented and ASCII characters
    text = unicodedata.normalize('NFKD', text).encode('ascii', 'ignore').decode('utf-8', 'ignore')
    # 3. Remove special characters
    words = re.sub(r"[^a-z0-9\s]", '', text).split()
    # 4. Tokenize
    tokenize = nltk.tokenize.ToktokTokenizer()
    tokenize.tokenize(text, return_str=False)
    # 5. Stemming or Lemmatizing
    if stem_or_lem == "stem":
        ps = nltk.porter.PorterStemmer()
        text = [ps.stem(word) for word in text.split()]
        ' '.join(text)
        print('Stemming Performed')
    elif stem_or_lem == "lem":
        wnl = nltk.stem.WordNetLemmatizer()
        text = [wnl.lemmatize(word) for word in text.split()]
        ' '.join(text)
        print('Lemmatizing Performed')
    else:
        print('No Stemming or Lemmatizing Performed')
    # 6. Remove StopWords
    stopwords = nltk.corpus.stopwords.words('english') + add_stopwords
    
    return [word for word in words if word not in stopwords]

