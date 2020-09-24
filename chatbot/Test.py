
import nltk
import numpy as np
import io
import string
import warnings
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import re
from flask import Flask, render_template, request
from flask_mail import Message, Mail

from chatbase import Message as MsgChat

warnings.filterwarnings('ignore')


f = open("info.txt","r", errors='ignore')
text = f.read()

def chatbot(user_response):

    sent_tokens = nltk.sent_tokenize(text)
    word_tokens = nltk.word_tokenize(text)

    lemmer = nltk.WordNetLemmatizer()

    def LemTokens(tokens):
        return [lemmer.lemmatize(token) for token in tokens]

    remove_punct_dict = dict((ord(punct), None) for punct in string.punctuation)

    def LemNormalize(txt):
        return LemTokens(nltk.word_tokenize(txt.lower().translate(remove_punct_dict)))

    def response(user_response):
        chatbot_response = ''
        sent_tokens.append(user_response)
        TfidfVec = TfidfVectorizer(tokenizer=LemNormalize, stop_words='english')
        tfidf = TfidfVec.fit_transform(sent_tokens)
        vals = cosine_similarity(tfidf[-1],tfidf)
        idx = vals.argsort()[0][-2]
        flat = vals.flatten()
        flat.sort()
        req = flat[-2]
        if(req==0):
            chatbot_response = chatbot_response + 'Sorry, cannot understand your query'
            return chatbot_response
        else:
            chatbot_response = chatbot_response+sent_tokens[idx]
            return chatbot_response

    flag = True

    
    while(flag):

        user_response = user_response.lower()
        if(user_response!= "bye"):
            bot_response = response(user_response)
            sent_tokens.remove(user_response)
            return(bot_response)
        else:
            flag = False
            return 'bye'

def not_handeled(user_response):
    msg = MsgChat(api_key= "6f6aa25c-e467-49f7-9799-67efb413b829",
            type= "user",
            platform= "web",
            message= user_response,
            version= "1.0",
            user_id= "user-404",
            not_handled= "true")
    resp = msg.send()
    print(resp)

def handeled(user_response):
    msg = MsgChat(api_key= "6f6aa25c-e467-49f7-9799-67efb413b829",
            type= "user",
            platform= "web",
            message= user_response,
            version= "1.0",
            user_id= "user-200"
    )
    resp = msg.send()
    print(resp)

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
    output = chatbot(user_input)
    if "Sorry, cannot understand your query" in output:
        not_handeled(user_input)
    else :
        handeled(user_input)
    return output

if __name__ == '__main__':
    app.run(debug=True, port=8081)
