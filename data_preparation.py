#import needed Libraries
import nltk
from nltk.stem.lancaster import  LancasterStemmer
stemmer =  LancasterStemmer()

import numpy as np
import random
import string

string_punctuation = string.punctuation
string_punctuation = (list(string_punctuation))

#load the data
import json

with open("/home/acer/PycharmProjects/CHATBOT/intents.json") as f:
    intents=json.load(f)
    print(intents)

    words = []
    documents = []
    classes = []
    for intent in intents['intents']:
        for pattern in intent['patterns']:
            w = nltk.word_tokenize(pattern.lower())
            words.extend(w)
            documents.append((w,intent['tag'].lower()))
            if intent['tag'].lower() not in classes:
                classes.append(intent['tag'])

    print(len(documents),documents)

    print(words)
    words = [stemmer.stem(w) for w in words if w not in string_punctuation]
    words = sorted(list(set(words)))
    print(len(words), words)

    print(classes)
    classes = sorted(list(set(classes)))
    print(len(classes),classes)


    #create our training data

    training = []
    output = []
    output_empty = [0]*len(classes)

    for doc in documents:
        bag= []
        pattern_words=doc[0]
        pattern_words = [stemmer.stem(w) for w in pattern_words]

        for w in words:
            if w in pattern_words:
                bag.append(1)
            else:
                bag.append(0)


        #BAG =======================PATTERN
        output_row =list(output_empty)
        output_row[classes.index(doc[1])] = 1
        #OUTPUT_ROW ==========================================TAG
        training.append([bag,output_row])

    print(training)
    random.shuffle(training)
    training = np.array(training)
    print(training)
    # print("HIIIII")

    train_x = list(training[:,0])##################PATTERN
    # print(train_x)
    train_y = list(training[:,1])#########################TAG
    # print(train_y)


    ##SAVE ALL OF OUR DATA STRUCTURE

    import pickle
    pickle.dump({'words':words,"classes":classes,'train_x':train_x,
                 'train_y':train_y},open("training_data","wb"))