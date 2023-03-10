import random
import json
import pickle
import numpy as np

import nltk
from nltk.stem import WordNetLemmatizer

import ssl

try:
    _create_unverified_https_context = ssl._create_unverified_context
except AttributeError:
    pass
else:
    ssl._create_default_https_context = _create_unverified_https_context

#nltk.download()
# AI stuff -> SIMPLE ANN (not ML nor RNN)
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Activation, Dropout
from tensorflow.keras.optimizers import SGD
import os
lemmatizer = WordNetLemmatizer()
intents = json.loads(open(os.path.join(os.path.dirname(os.path.dirname(__file__)),'ChatBot/intents.json')).read())


words = []
classes = []
documents = []
ignore_letters = ['?','!','.',',']

# Put all words on a list
for intent in intents['intents']:
    for pattern in intent['patterns']:
        word_list = nltk.word_tokenize(pattern.lower())
        words.extend(word_list)
        documents.append((word_list,intent['tag']))
        if intent['tag'] not in classes:
            classes.append(intent['tag'])
            
# Clean unnecesary (repeated/sign) items  
words = [lemmatizer.lemmatize(word) for word in words if word not in ignore_letters]
words = sorted(set(words))
classes = sorted(set(classes))

# Store all Data in Files
pickle.dump(words, open(os.path.join(os.path.dirname(os.path.dirname(__file__)),'ChatBot\Model\words.pkl'), 'wb'))
pickle.dump(classes, open(os.path.join(os.path.dirname(os.path.dirname(__file__)),'ChatBot\Model\classes.pkl'), 'wb'))

training = []
output_empty = [0] * len(classes)

# Prepare data for training
for document in documents:
    bag = []
    word_patterns = document[0]
    word_patterns = [lemmatizer.lemmatize(word.lower()) for word in word_patterns]
    for word in words:
        bag.append(1) if word in word_patterns else bag.append(0)
        
    output_row = list(output_empty)
    output_row[classes.index(document[1])] = 1
    training.append([bag, output_row])
    
random.shuffle(training)
training = np.array(training)

train_x = list(training[:,0])
train_y = list(training[:,1])

# Neural Network
model = Sequential()
# INPUT LAYER + HIDDEN LAYER -> train_x is num of inputs
model.add(Dense(256, input_shape=(len(train_x[0]),), activation='relu'))
model.add(Dropout(0.5))
model.add(Dense(128, activation='relu'))
model.add(Dropout(0.5))
# OUTPUT LAYER -> train_y is num of outputs
model.add(Dense(len(train_y[0]), activation='softmax'))

sgd = SGD(lr=0.01,momentum=0.9,nesterov=True)
model.compile(loss='categorical_crossentropy', optimizer=sgd, metrics=['accuracy'])

hist = model.fit(np.array(train_x), np.array(train_y), epochs=200, batch_size=5, verbose=1)
model.save(classes, os.path.join(os.path.dirname(os.path.dirname(__file__)),'ChatBot/Model/chatbotmodel.h5'), hist)
print("Done")