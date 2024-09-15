import random
import json
import pickle
import numpy as np
import nltk
from nltk.stem import WordNetLemmatizer
import tensorflow as tf

lemmatizer = WordNetLemmatizer()

intents = json.load(open('intents.json'))

# load what we did in reading binary mode
words = pickle.load(open('words.pkl', 'rb'))
classes = pickle.load(open('classes.pkl', 'rb'))
model = tf.keras.models.load_model('chatbot_model.h5')

def clean_up_sentence(sentence):
    #tokenize the sentence and words in the sentence
    sentence = sentence.lower()
    sentence_words = nltk.word_tokenize(sentence)
    sentence_words = [lemmatizer.lemmatize(word) for word in sentence_words]
    return sentence_words

#convert a sentence into 0 and 1 that indicate if the word is in the sentence
def bag_of_words(sentence):
    sentence_words = clean_up_sentence(sentence)
    bag = [0] * len(words)
    for palabra in sentence_words:
        for i, word in enumerate(words):
            if word == palabra:
                bag[i] = 1
    return np.array(bag)


def predict_class(sentence):
    bagOfWords = bag_of_words(sentence)
    res = model.predict(np.array([bagOfWords]))[0]
    #uncertainty
    ERROR_THRESHOLD = 0.25

    results = [[i, result] for i, result in enumerate(res) if result > ERROR_THRESHOLD]


    #highest probability first
    results.sort(key=lambda x: x[1], reverse=True)
    return_list = []

    #for result in results:
        #return_list.append({'intent': classes[result[0]], 'probability': str(result[1])})

    if results:
        for result in results:
            return_list.append({'intent': classes[result[0]], 'probability': str(result[1])})
    else:
        return_list.append({'intent': 'no_entendido', 'probability': '0'})

    return return_list


def get_response(intents_list, intents_json):
    tag = intents_list[0]['intent']
    list_of_intents = intents_json['intents']

    result = "Lo siento, no entiendo lo que quieres decir."

    for i in list_of_intents:
        if i['tag'] == tag:
            result = random.choice(i['responses'])
            break

    return result

print('Habla con tu asistente virtual! Recuerda que al hablar con él estás aceptando nuestro Aviso de Privacidad')
print('Le puedes hacer preguntas como: Que servicios ofrece Banorte?, Como activar mi tarjeta de credito Banorte?, Como solicitar un credito en Banorte?, etc.')

while True:
    message = input('\nTu: ')
    ints = predict_class(message)
    res = get_response(ints, intents)
    print(f'Asistente virtual: {res}')

    if ints and ints[0]['intent'] == 'despedida':
        print("\nEstas seguro que quieres salir? (si/no): ")
        res = input()
        if res == 'si' or res == 's' or res == 'yes' or res == 'y' or res == 'Si' or res == 'S' or res == 'Yes' or res == 'Y'or res == 'SI' or  res == 'YES':
            break
        else:
            continue