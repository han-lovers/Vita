import random
import json
import pickle
import numpy as np
import nltk
from nltk.stem import WordNetLemmatizer #misma palabra para solo stem
import tensorflow as tf
import keras
from keras import layers
from tensorflow.keras import layers, models
#from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Activation, Dropout
from tensorflow.keras.optimizers import SGD

lemmatizer = WordNetLemmatizer()

intents = json.loads(open('intents.json').read())

words = []
classes = []
documents = []
ignore_letters = ['?' , '!' , '.' , ',']

for intent in intents['intents']:
    for pattern in intent['patterns']:
        #getting text and splits it up
        word_list = nltk.word_tokenize(pattern)
        words.extend(word_list)
        #the word lists belong to the task
        documents.append((word_list, intent['tag']))
        if intent['tag'] not in classes:
            classes.append(intent['tag'])

# lemmatizes the words and removes the ignore letters
words= [lemmatizer.lemmatize(word) for word in words if word not in ignore_letters]
words=sorted(set(words))

print(words)
