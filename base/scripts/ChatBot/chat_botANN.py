import random
import json
import pickle
import numpy as np

import nltk
import ssl
from nltk.stem import WordNetLemmatizer

from tensorflow.keras.models import load_model

# SEND AN EMAIL
#import yagmail
user = 'machinesfromhell@gmail.com'
app_password = 'eiepjrzxegzxuahw' # a token for gmail
to = 'townespartana@gmail.com'
subject = 'LUCHO! Tu robot Personal te necesita'
content = [
    ['Mira te lo digo todo de una...','Estaba hablando con uno de mis clientes y todo normal, despues me di cuante de algo rerisimo que dijeron es por eso que te digo...','Podes ir a ver que dijo de verdad plis, Gracias Luchongo'],
    ["Hola Luchongo, como esta la casa? Espero que Juan se porte bien...","Tuve un problema con uno de los clientes","Me escribieron esto: "], 
    ["Hola Lucho, perdon por molestar a esta hore pero necesito que me veas algo que paso con un cliente","El me dijo esto y no se que significa: "],
    ["Aloha Lucho, como va todo, chilling o al palo? ","Me llego un mensaje con unos de los clientes y ni idea boludo lo que me mando el botija","Me dijo esto: "],
    ["Che boludo un botija cliente me escribio algo y no entendi ni un sorete, fijate esto: "],
    ["I fucked it up, ","Uno de los clientes me dijo algo y no entendi", "Checkealo: "]
    ]

# OS STUFF
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
try:
    _create_unverified_https_context = ssl._create_unverified_context
except AttributeError:
    pass
else:
    ssl._create_default_https_context = _create_unverified_https_context
nltk.download('punkt')
nltk.download('wordnet')

lemmatizer = WordNetLemmatizer()
#intents = json.loads(open('intents.json').read())

#words = pickle.load(open('Model/words.pkl', 'rb'))
#classes = pickle.load(open('Model/classes.pkl', 'rb'))
#model = load_model('Model/chatbotmodel.h5')
#clean_up_sentence("Hola, como te va?")

class Chatbot():
    def __init__(self):
        super().__init__()
        self.lemmatizer = WordNetLemmatizer()
        self.intents = json.loads(open(os.path.join(os.path.dirname(os.path.dirname(__file__)),'ChatBot/intents.json')).read())

        self.words = pickle.load(open(os.path.join(os.path.dirname(os.path.dirname(__file__)),'ChatBot/Model/words.pkl'),'rb'))
        self.classes = pickle.load(open(os.path.join(os.path.dirname(os.path.dirname(__file__)),'ChatBot/Model/classes.pkl'),'rb'))
        self.model = load_model(os.path.join(os.path.dirname(os.path.dirname(__file__)),'ChatBot/Model/chatbotmodel.h5'))
        print("HEllo")
        try:
            _create_unverified_https_context = ssl._create_unverified_context
        except AttributeError:
            pass
        else:
            ssl._create_default_https_context = _create_unverified_https_context
        nltk.download('punkt')
        nltk.download('wordnet')
    # Clean up
    def clean_up_sentence(self, sentence):
        sentence_words = nltk.word_tokenize(sentence)
        sentence_words = [self.lemmatizer.lemmatize(word) for word in sentence_words]
        return sentence_words

    # Convert words into numbers to analize
    def bag_of_words(self, sentence):
        sentence_words = self.clean_up_sentence(sentence)
        bag = [0] * len(self.words)
        for w in sentence_words:
            for i, word in enumerate(self.words):
                if word == w:
                    bag[i] = 1
                    
        return np.array(bag)

    # Predict the words is going to say
    def predict_class(self, sentece):
        # Predict
        bow = self.bag_of_words(sentece)
        res = self.model.predict(np.array([bow]))[0]
        ERROR_THRESHOLD = 0.25
        results = [[i,r] for i, r in enumerate(res) if r > ERROR_THRESHOLD]
        
        # Use word with highest probability
        results.sort(key=lambda x: x[1], reverse=True)
        return_list = []
        # Apend word to sentences
        print(results)
        for r in results:
            # If you are not sure, don't say anything
            if float(r[1]) <= 0.60:
                return_list.append({'intent': "noanswer", 'probobility':"1.0"})
            else:
                return_list.append({'intent': self.classes[r[0]], 'probobility':str(r[1])})
        return return_list

    # Think of a response -> Choose random
    def get_response(self, intents_list, intents_json):
        tag = intents_list[0]['intent']
        print(tag)
        result = ""
        list_of_intents = intents_json['intents']
        for i in list_of_intents:
            if i['tag'] == tag:
                print(i['tag'])
                print(i['responses'])
                result = random.choice(i['responses'])
                break
        print(result)
        return result, tag

    def Talking(self, message):
        ints = self.predict_class(message.lower())
        # res -> Answer |  tag -> Topic
        res, tag = self.get_response(ints, self.intents)
        if tag == "noanswer":
            print("NONAWNSER")
            """
            with yagmail.SMTP(user, app_password) as yag:
                yag.send(to, subject, content[random.randint(0,5)] + [message])
            """
        return [res, tag]


"""
import csv
while True:
    message = input(">> ")
    ints = predict_class(message.lower())
    res,tag = get_response(ints, intents)

    # If you are offered pesos
    if tag == "tengo":
        oferta_pesos(message)
    
    print( res)
"""