import pickle
import json
import nltk
import numpy as np
import tflearn
import tensorflow as tf
import random
from nltk.stem.lancaster import  LancasterStemmer
stemmer =  LancasterStemmer()



data = pickle.load(open('/home/acer/PycharmProjects/CHATBOT/test/training_data',"rb"))
print(data)

words = data['words']
classes = data['classes']
train_x = data['train_x']
train_y = data['train_y']


##BUILD MODEL

tf.reset_default_graph()
###build neural network
net = tflearn.input_data(shape=[None,len(train_x[0])])
net = tflearn.fully_connected(net,8)
net = tflearn.fully_connected(net,8)
net = tflearn.fully_connected(net,len(train_y[0]),activation='softmax')
net = tflearn.regression(net)

###define model and setup tensorboard

model = tflearn.DNN(net,tensorboard_dir='tflearn_logs')
###start training (apply gradient descent algorithm

# model.fit(train_x,train_y,n_epoch=1000,batch_size=8,show_metric=True)
# model.save('model.tflearn')


#import Json

with open('/home/acer/PycharmProjects/CHATBOT/intents.json') as json_data:
    intents = json.load(json_data)
    print(intents)


    ##LOAD OUR SAVED model
    model.load('./model.tflearn')

    def clean_up_sentence(sentence):
        sentence_Words =nltk.word_tokenize(sentence)
        sentence_Words =[stemmer.stem(w) for w in sentence_Words ]
        return  sentence_Words

    def bow(sentence,words,show_details=False):
        sentence_words = clean_up_sentence(sentence)
        print(sentence_words)
        bag = [0] * len(words)
        for s in sentence_words:
            for i,w in enumerate(words):
                if w == s:
                    bag[i] = 1
                    if show_details:
                        print("found in bag:%s" % w)
        return (np.array(bag))

    p = bow("is your shop open today?",words)
    print(p)
    ERROR_THRESHOLD = 0.25
    def classify(sentence):
        bag_words = bow(sentence,words)
        results=model.predict([bag_words])[0]
        print(results)
        results = [[i,r] for i,r in enumerate(results) if r> ERROR_THRESHOLD]
        print(results)
        results.sort(key=lambda x:x[1],reverse=True)
        print(results,"g")
        return_list = []
        for r in results:
            return_list.append((classes[r[0]],r[1]))
        print(return_list)

        return return_list




    def response(sentence):
        result = classify(sentence)
        if result:
            print(result[0][0])
            while result:
                for i in intents['intents']:
                    if i['tag'] == result[0][0]:
                        return random.choice(i['responses'])

                result.pop(0)
    # result=response("who are you")
    # print(result)




