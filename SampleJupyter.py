#! C:\Users\Shubham Gupta\AppData\Local\Programs\Python\Python39\python.exe
# coding: utf-8

# In[2]:

import sys
import os
import numpy as np

import pandas as pd

def add_unique_postfix(fn):
    if not os.path.exists(fn):
        return fn

    path, name = os.path.split(fn)
    name, ext = os.path.splitext(name)

    make_fn = lambda i: os.path.join(path, '%s(%d)%s' % (name, i, ext))

    for i in range(2, sys.maxsize):
        uni_fn = make_fn(i)
        if not os.path.exists(uni_fn):
            return uni_fn

    return None



filename_read = sys.argv[1]
#print(filename_read)

#quit()
fn_unique = add_unique_postfix('result/result.csv')


sys.stdout = open(fn_unique, 'w')

df = pd.read_csv(filename_read)
df.head()

# In[3]:
df.shape

# In[4]:
df['Sentiment'].value_counts() #positive, negative , neutral


# In[6]:
import nltk
#nltk.download('punkt')

from nltk import word_tokenize

#data = "Covid 19 sample data analysis is very difficult (also known as hard) and time consuming."
#print(word_tokenize(data))


# In[7]:

#nltk.download('stopwords')
from nltk.corpus import stopwords
stopwords = set(stopwords.words('english'))
#print(stopwords)


# In[8]:

import string 


# In[10]:
from sklearn.feature_extraction.text import CountVectorizer


# In[12]:
#nltk.download('stopwords')
from nltk.corpus import stopwords
def text_cleaning(a):
    remove_punctuation = [char for char in a if char not in string.punctuation]
    #print(remove_punctuation)
    remove_punctuation=''.join(remove_punctuation)
    #print(remove_punctuation)
    return [word for word in remove_punctuation.split() if word.lower() not in stopwords.words('english')]


# In[13]:
df.head()

# In[14]:
#print(df.iloc[:,2].apply(text_cleaning))

# In[15]:
from sklearn.feature_extraction.text import CountVectorizer
bow_transformer = CountVectorizer(analyzer=text_cleaning).fit(df['Tweet'])

#print(len(bow_transformer.vocabulary_))
bow_transformer.vocabulary_


# In[16]:
title_bow = bow_transformer.transform(df['Tweet'])
#print(title_bow)


# In[17]:
x = title_bow.toarray()
#print(x)

x.shape


# In[18]:


from sklearn.feature_extraction.text import TfidfTransformer
tfidf_transformer = TfidfTransformer().fit(title_bow)
#print(tfidf_transformer)

title_tfidf = tfidf_transformer.transform(title_bow)
#print(title_tfidf)
#print(title_tfidf.shape)


# In[19]:


from sklearn.naive_bayes import MultinomialNB
model = MultinomialNB().fit(title_tfidf, df['Sentiment'])
#model_1 = MultinomialNB().get_params(['Tweet'])
#print(model_1)


# In[20]:
all_predictions = model.predict(title_tfidf)
#print(all_predictions)

# In[21]:
from sklearn.metrics import confusion_matrix

confusion_matrix(df['Sentiment'], all_predictions)


# In[22]:

from sklearn.metrics import classification_report

report = classification_report(all_predictions,df['Sentiment'])
# print(report)

def classification_report_csv(report):
    report_data = []
    lines = report.split('\n')
    #print(lines)
    for line in lines[2:5]:
        if line.strip():
            #print(line)
            row = {}
            row_data = line.split()
            #print(row_data)
            row['class'] = row_data[0].strip()
            row['precision'] = float(row_data[1].strip())
            row['recall'] = float(row_data[2].strip())
            row['f1_score'] = float(row_data[3].strip())
            row['support'] = float(row_data[4].strip())
            report_data.append(row)
    dataframe = pd.DataFrame.from_dict(report_data)
    dataframe.to_csv(fn_unique, index = False)


classification_report_csv(report)
# In[23]:
from sklearn.metrics import accuracy_score

#print(accuracy_score(all_predictions,df['Sentiment']))

sys.stdout.close()

sys.exit(fn_unique)
