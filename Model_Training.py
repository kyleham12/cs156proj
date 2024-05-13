#!/usr/bin/env python
# coding: utf-8

# In[383]:


import pandas as pd
import nltk


# In[384]:


df = pd.read_csv("spotify_millsongdata.csv")


# In[385]:


df.head(5)


# In[386]:


df.tail(5)


# In[387]:


df.shape


# In[388]:


df.isnull().sum()


# In[389]:


df =df.sample(5000).drop('link', axis=1).reset_index(drop=True)


# In[390]:


df.head(10)


# In[391]:


df['text'][0]


# In[392]:


# df = df.sample(5000)


# In[393]:


df.shape


# Text Cleaning/ Text Preprocessing

# In[394]:


df['text'] = df['text'].str.lower().replace(r'^\w\s', ' ').replace(r'\n', ' ', regex = True)


# In[395]:


df = df.assign(feedback=0)


# In[396]:


import nltk
from nltk.stem.porter import PorterStemmer
stemmer = PorterStemmer()

def tokenization(txt):
    tokens = nltk.word_tokenize(txt)
    stemming = [stemmer.stem(w) for w in tokens]
    return " ".join(stemming)


# In[397]:


df['text'] = df['text'].apply(lambda x: tokenization(x))


# In[398]:


from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


# In[399]:


tfidvector = TfidfVectorizer(analyzer='word',stop_words='english')
matrix = tfidvector.fit_transform(df['text'])
similarity = cosine_similarity(matrix)


# In[400]:


similarity[0]


# In[401]:


df[df['song'] == df.iloc[0]['song']]


# In[402]:


from sklearn.model_selection import train_test_split
from sklearn.svm import SVC
from sklearn.metrics import confusion_matrix
from sklearn.metrics import classification_report
import numpy as np
from scipy.sparse import hstack, csr_matrix


# In[403]:


df['combined_text'] = df['artist'] + ' ' + df['song'] + ' ' + df['text']
tfid_X = tfidvector.fit_transform(df['combined_text'])

df['feedback'] = np.random.choice([-1, 0, 1], size=len(df))

y = df['feedback']

X_train, X_test, y_train, y_test = train_test_split(tfid_X, y, test_size=0.2, random_state=42)

svc = SVC(probability=True)
svc.fit(X_train, y_train)

train_score = svc.score(X_train, y_train)
test_score = svc.score(X_test, y_test)


# In[404]:


print("Training accuracy:", train_score)
print("Testing accuracy:", test_score)


# In[405]:


ypred = svc.predict(X_test)

cm = confusion_matrix(y_test, ypred)
print(cm)


# In[406]:


cr = classification_report(y_test, ypred)
print(cr)


# In[407]:


def recommendation(song_df, svc_model):
    idx = df[df['song'] == song_df].index[0]
    distances = sorted(list(enumerate(similarity[idx])),reverse=True,key=lambda x:x[1])
    
    recommended_songs = []
    song_probs = []
    
    for m_id in distances[1:21]:
        artist = df.iloc[m_id[0]]['artist']
        song = df.iloc[m_id[0]]['song']
        text = df.iloc[m_id[0]]['text']
        
        combo = f"{artist} {song} {text}"
        X = tfidvector.fit_transform([combo])

        num_columns_to_add = tfid_X.shape[1] - X.shape[1]

        zeros_matrix = csr_matrix((X.shape[0], num_columns_to_add), dtype=np.float64)

        X = hstack([X, zeros_matrix])
    
        probability = svc_model.predict_proba(X)[0][1]
        song_probs.append(probability)
    
    sorted_indices = sorted(range(len(song_probs)), key=lambda i: song_probs[i], reverse=True)
    sorted_songs = [distances[i+1][0] for i in sorted_indices]
    
    recommended_songs = [df.iloc[i]['song'] for i in sorted_songs]
    
    return recommended_songs


# In[409]:


recommendation(df.iloc[0]['song'], svc)


# 

# In[410]:


def update_model(return_info):
    for row in return_info:
        song_name = row[0]
        feedback_value = row[2]
        df.loc[df['song'] == song_name, 'feedback'] = feedback_value

    df['combined_text'] = df['artist'] + ' ' + df['song'] + ' ' + df['text']
    tfid_X = tfidvector.fit_transform(df['combined_text'])

    df['feedback'] = np.random.choice([-1, 0, 1], size=len(df))

    y = df['feedback']

    X_train, X_test, y_train, y_test = train_test_split(tfid_X, y, test_size=0.2, random_state=42)

    svc = SVC(probability=True)
    svc.fit(X_train, y_train)

    return svc


# In[411]:


import pickle
pickle.dump(similarity,open('similarity.pkl','wb'))
pickle.dump(df,open('df.pkl','wb'))
pickle.dump(svc,open('svc.pkl','wb'))


# In[412]:


df.head()

