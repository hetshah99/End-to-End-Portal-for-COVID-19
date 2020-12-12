import nltk
from nltk.stem import WordNetLemmatizer
lemmatizer = WordNetLemmatizer()
import pickle
import numpy as np
from flask import Flask, render_template, request
from flask_mail import Message, Mail
import nltk
from sklearn import metrics
import pandas as pd
import numpy as np 
import matplotlib as mpl
import matplotlib.pyplot as plt
from collections import Counter
from subprocess import check_output
from wordcloud import WordCloud, STOPWORDS
from sklearn.cluster import KMeans
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.naive_bayes import MultinomialNB
from sklearn.model_selection import GridSearchCV
from sklearn.pipeline import Pipeline
from nltk.stem import PorterStemmer
from nltk.corpus import stopwords

from keras.models import load_model
model = load_model('chatbot_model.h5')
import json
import random
intents = json.loads(open('intents.json',encoding="utf8").read())
words = pickle.load(open('words.pkl','rb'))
classes = pickle.load(open('classes.pkl','rb'))


def clean_up_sentence(sentence):
    sentence_words = nltk.word_tokenize(sentence)
    sentence_words = [lemmatizer.lemmatize(word.lower()) for word in sentence_words]
    return sentence_words


def bow(sentence, words, show_details=True):
    sentence_words = clean_up_sentence(sentence)
    bag = [0]*len(words)
    for s in sentence_words:
        for i,w in enumerate(words):
            if w == s:
                bag[i] = 1
                if show_details:
                    print ("found in bag: %s" % w)
                
    return(np.array(bag))

def predict_class(sentence, model):
    p = bow(sentence, words,show_details=False)
    res = model.predict(np.array([p]))[0]
    print(res)
    ERROR_THRESHOLD = 0.25
    results = [[i,r] for i,r in enumerate(res) if r>ERROR_THRESHOLD]
    print(results)
    results.sort(key=lambda x: x[1], reverse=True)
    return_list = []
    for r in results:
        return_list.append({"intent": classes[r[0]], "probability": str(r[1])})
    return return_list

def getResponse(ints, intents_json):
    tag = ints[0]['intent']
    list_of_intents = intents_json['intents']
    for i in list_of_intents:
        if(i['tag']== tag):
            result = random.choice(i['responses'])
            break
    return result

def chatbot_response(msg):
    ints = predict_class(msg, model)
    res = getResponse(ints, intents)
    return res







training_set = pd.read_csv("train_covid.csv")


print(training_set)
training_set = training_set[(training_set.label == 'FAKE') | (training_set.label == 'REAL')]





training_set_labels = training_set.label 
training_set_data = training_set.drop("label", axis = 1)
training_set_data = training_set_data.drop("ID", axis = 1)



training_set_data["full_text"] = training_set_data["title"].map(str) + " " + training_set_data["text"]
training_data = training_set_data["full_text"]



stopwords = set(STOPWORDS)




training_labels = training_set_labels.tolist()

training_labels

labels = [1 if x =='FAKE' else 0 for x in training_labels]

from nltk.stem import PorterStemmer
from nltk.corpus import stopwords
stop_list = stopwords.words('english')
stemmer = PorterStemmer()
all_tokens_lower = [t.lower() for t in training_data]
tokens_normalised = [stemmer.stem(t) for t in all_tokens_lower
                                     if t not in stop_list]


X_train, X_test, y_train, y_test = train_test_split(tokens_normalised, labels,test_size = 0.3, random_state = 42 )





X_train = np.asarray(X_train)
y_train = np.asarray(y_train)
X_test = np.asarray(X_test)
y_test = np.asarray(y_test)


text_clf = Pipeline([('vect', CountVectorizer(stop_words = "english")), ('tfidf', TfidfTransformer()), ('clf', MultinomialNB())])
parameters = {'vect__ngram_range': [(1, 1), (1, 2), (1, 3)], 
              'tfidf__use_idf': (True, False), 
              'tfidf__norm': ('l1', 'l2'), 
              'tfidf__sublinear_tf': (True, False), 
              'clf__alpha': (1e-2, 1e-3)
             }




gs_clf = GridSearchCV(text_clf, parameters, n_jobs=-1, cv=5)

model1 = gs_clf.fit(X_train, y_train)


predicted = model1.predict(X_test)

np.mean(predicted == y_test)


def chatbot_response1(msg):
    testing_set = pd.read_csv("test.csv", sep=',')
    testing_set_data = testing_set.drop("ID", axis = 1)
    testing_set_data["full_text"] = msg
    test_data = testing_set_data["full_text"]
    stop_list = stopwords.words('english')
    stemmer = PorterStemmer()
    all_tokens_lower = [t.lower() for t in test_data]
    tokens_normalised1 = [stemmer.stem(t) for t in all_tokens_lower if t not in test_data]
    
    final_testX = np.asarray(tokens_normalised1)
    print(final_testX.shape)
    predictedfinal = model1.predict(final_testX)
    results =  predictedfinal
    results = ['FAKE' if x ==1 else 'REAL' for x in results]
    return results


import tkinter
from tkinter import *


app = Flask(__name__)



def word_count(string):
    tokens = string.split()
    n_tokens = len(tokens)
    return n_tokens 

@app.route('/')
def index():
    return render_template('firstpage.html')



@app.route('/home')
def home():
    return render_template('firstpage.html')

@app.route('/get')# methods=['POST'])
def process():
    user_input = request.args.get("user_input")
    if word_count(user_input) < 3:
        return ("Sorry, in order to get the best response possible, your query must be at least three words long.")
    output = chatbot_response(user_input)
   
    return output


@app.route('/get1')# methods=['POST'])
def process1():
    user_input = request.args.get("user_input")
    if word_count(user_input) < 3:
        return ("Sorry, in order to get the best response possible, your query must be at least three words long.")
    output = chatbot_response1(user_input)
    print(output)
    return str(output)

if __name__ == '__main__':
    app.run(debug=False, port=8080)

