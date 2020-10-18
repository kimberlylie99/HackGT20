import numpy as np 
import pandas as pd 
import re
import os
import nltk 
import matplotlib.pyplot as plt
import urllib
from sklearn import model_selection, naive_bayes, svm
from sklearn.metrics import accuracy_score
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score


def processFeatures(features):
    new_features = []
    for sentence in range(0, len(features)):
        # Remove all the special characters
        processed_feature = re.sub(r'\W', ' ', str(features[sentence]))

        # remove all single characters
        processed_feature= re.sub(r'\s+[a-zA-Z]\s+', ' ', processed_feature)

        # Remove single characters from the start
        processed_feature = re.sub(r'\^[a-zA-Z]\s+', ' ', processed_feature) 

        # Substituting multiple spaces with single space
        processed_feature = re.sub(r'\s+', ' ', processed_feature, flags=re.I)

        # Removing prefixed 'b'
        processed_feature = re.sub(r'^b\s+', '', processed_feature)

        # Converting to Lowercase
        processed_feature = processed_feature.lower()

        new_features.append(processed_feature)
    return new_features
    

def getClass(stringList):
    THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))
    my_file = os.path.join(THIS_FOLDER, 'hackgt20_data.csv')
    company_review = pd.read_csv(my_file, encoding='windows-1252')
    company_review.head()
    features = company_review.iloc[:, 2].values
    labels = company_review.iloc[:, 1].values
    #processed_features = []
    predictions = []
    for i in range(len(stringList)):
        if(len(stringList[i]) <= 5 or 'will notify' in stringList[i] or ('information' in stringList[i] and not('collect' in stringList[i]) ) or 'does not share' in stringList[i] or 'with your consent' in stringList[i] ):
            predictions.append('Positive')
            continue
        if('class action' in stringList[i].lower() or 'cookies' in stringList[i].lower() or 'indemnify' in stringList[i].lower() or 'log info' in stringList[i] or 'ip address' in stringList[i].lower()):
            predictions.append('Negative')
            continue
        sen = stringList[i]
        featuresNew = features + sen
        processedfeatures = processFeatures(featuresNew)
        
        vectorizer = TfidfVectorizer (max_features=100, min_df=2, max_df=1.0, stop_words=stopwords.words('english'))
        processedfeatures = vectorizer.fit_transform(processedfeatures).toarray()
        X_train, X_test, y_train, y_test = train_test_split(processedfeatures, labels, test_size=0.2, random_state=0)
        text_classifier = RandomForestClassifier(n_estimators=200, random_state=0)
        text_classifier.fit(X_train, y_train)

        arr = processedfeatures[processedfeatures.shape[0]-1,:]
        arr = np.reshape(arr, (1,processedfeatures.shape[1]))
        predictions.append(text_classifier.predict(arr)[0])
        
    #make the dictionary to return 
    listToReturn = []
    for i in range(len(stringList)):
        dictNew={}
        dictNew['text'] = stringList[i]
        if(predictions[i] == 'Negative'):
            dictNew['label'] = False
        else:
            dictNew['label'] = True
        listToReturn.append(dictNew)
    return listToReturn
    
    