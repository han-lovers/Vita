import random
import json
import pickle
import numpy as np
import nltk
from nltk.stem import WordNetLemmatizer #misma palabra para solo stem
import keras
from tensorflow.keras import layers, models
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
        word_list = nltk.word_tokenize(pattern.lower())
        words.extend(word_list)
        #the word lists belong to the task
        documents.append((word_list, intent['tag']))
        if intent['tag'] not in classes:
            classes.append(intent['tag'])

# lemmatizes the words and removes the ignore letters
words= [lemmatizer.lemmatize(word) for word in words if word not in ignore_letters]
words=sorted(set(words))

#print(words)

classes = sorted(set(classes))

# save the words and classes in a pickle file to transport data on the network and mantain the thing across sesions
pickle.dump(words, open('words.pkl', 'wb'))
pickle.dump(classes, open('classes.pkl', 'wb'))

training = []
output_empty = [0] * len(classes)

for document in documents:
    bag = []
    # obtain the word patterns for each document
    word_patterns = document[0]
    # lemmatize each word in the word patterns
    word_patterns = [lemmatizer.lemmatize(word.lower()) for word in word_patterns]

    # create the bag of words depending on whether the word is in the word patterns
    for word in words:
        bag.append(1) if word in word_patterns else bag.append(0)

    # create the output row with the same lenght of the number of classes
    output_row = list(output_empty)
    #marks with 1 the position of the class in the output row
    output_row[classes.index(document[1])] = 1
    training.append([bag, output_row])

# shuffle the training data
random.shuffle(training)
training = np.array(training, dtype=object)

# create the train_x and train_y to divide the data of the bag and output row
#train_x = list(training[:, 0])
#train_y = list(training[:, 1])

train_x = np.array([item[0] for item in training])
train_y = np.array([item[1] for item in training])

#
model = keras.Sequential()
model.add(keras.Input(shape=(len(train_x[0]),)))
#128 neuronas relacionadas con capa de entrada anterior
# relu activa cada entrada en n max (0, x) para no linealidad y para patrones más complejos
model.add(Dense(128, activation='relu'))
#  drop out para evitar sobreajuste. apaga 50% de las neuronas para que no se ajuste demasiado
model.add(Dropout(0.5))
# reduce espacio para representación más estracta
model.add(Dense(64, activation='relu'))
model.add(Dropout(0.5))
# capa salida para salidas en forma de probabilidad
model.add(Dense(len(train_y[0]), activation='softmax'))

# determina qué tan grandes son los pasos que da el optimizador al actualizar los pesos.
initial_learning_rate = 0.01
decay_steps = 100000
decay_rate = 1e-6
# la tasa de aprendizaje disminuye inversamente con el número de pasos
learning_rate_schedule = keras.optimizers.schedules.InverseTimeDecay(initial_learning_rate, decay_steps, decay_rate)

# optimizador de descenso de gradiente estocástico, suaviza el proceso de optimización
sgd = SGD(learning_rate=learning_rate_schedule, momentum=0.9, nesterov=True)
# calcula diferencia entre probabilidades predichas y las verdaderas
model.compile(loss='categorical_crossentropy', optimizer=sgd, metrics=['accuracy'])
hist = model.fit(np.array(train_x), np.array(train_y), epochs=200, batch_size=5, verbose=1)

model.save('chatbot_model.h5', hist)