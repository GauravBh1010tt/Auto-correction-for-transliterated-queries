# -*- coding: utf-8 -*-
import nltk
import keras
import itertools
import numpy as np
import pickle
from keras.models import Sequential, Model
from keras.optimizers import RMSprop
from nltk.tokenize import regexp_tokenize
from keras.models import model_from_json
from keras.layers import Dense, Dropout, Activation, Lambda, Input,Embedding
from keras.layers import TimeDistributed,LSTM
 
class LossHistory(keras.callbacks.Callback):
    def on_train_begin(self, logs={}):
        self.losses = []

    def on_batch_end(self, batch, logs={}):
        self.losses.append(logs.get('loss'))

class dllm:  
    
    def __init__(self,vocab_size,step,batch_size,nb_epoch,embed_dims):    
        self.START = '$_START_$'
        self.END = '$_END_$'
        self.unk_token = '$_UNK_$'
        self.vocab_size = vocab_size
        self.step = step
        self.embedding_dims = embed_dims
        self.batch_size = batch_size
        self.nb_epoch = nb_epoch
        self.X_data = []
        self.y_data = []
        self.vocab = {}
        self.char_indices = []
        self.indices_char = []
        self.avg_loss = 0
        self.history=[]
        try:
            with open('history','rb')as h:
                loss = pickle.loads(h.read())
            avg_loss = (max(loss)+min(loss))/2
            self.rho = avg_loss/2
        except:
            self.rho = 4
            pass

    def prepare_data(self,data=False,re_train=False):
        
        flag = True
        if data==False:
            '''a=open('manner.xml').readlines()
            sent = []
            for k in a:
                k=k.lower()
                st = k.find('<subject>')
                if st==-1:
                    continue
                end = k.find('</subject>')
                sent.append(k[st+9:end-1])
                data = sent'''
            with open('question.pkl','rb')as h:
                data = pickle.loads(h.read())
            flag = False
        #print data[0:5]     
        sentence = ["%s %s %s" % (self.START,x,self.END) for x in data]
        tokenize_sent = [regexp_tokenize(x, 
                                         pattern = '\w+|$[\d\.]+|\S+') for x in sentence]
        
        freq = nltk.FreqDist(itertools.chain(*tokenize_sent))
        print 'found ',len(freq),' unique words'
        if self.vocab_size > len(freq):
            self.vocab_size = len(freq)
        self.vocab = freq.most_common(self.vocab_size - 3)
        index_to_word = [x[0] for x in self.vocab]
        index_to_word.append(self.unk_token)
        index_to_word.append(self.START)
        index_to_word.append(self.END)
        
        word_to_index = dict([(w,i) for i,w in enumerate(index_to_word)])
        
        for i,sent in enumerate(tokenize_sent):
            tokenize_sent[i] = [w if w in word_to_index else self.unk_token for w in sent]
        
        self.char_indices = word_to_index
        self.indices_char = index_to_word
        
        if re_train == True or flag==True:
            sentences = []
            next_chars = []
            sentences_f = []
            sentences_b = []
            next_chars_f = []
            next_chars_b = []
            
            for sent in tokenize_sent:
                temp = [self.START for i in range(self.step)]
                flag = False
                for word in sent:
                    temp.remove(temp[0])
                    temp.append(word)
                    if flag == True:
                        next_chars_f.append(word)
                    if word!=self.END:
                        temp1 = []
                        for i in temp:
                            temp1.append(i)
                        sentences_f.append(temp1)
                    flag = True
            
            for sent in tokenize_sent:
                temp = [self.END for i in range(self.step)]
                flag = False
                for word in sent[::-1]:
                    temp.remove(temp[0])
                    temp.append(word)
                    if flag == True:
                        next_chars_b.append(word)
                    if word!=self.START:
                        temp1 = []
                        for i in temp:
                            temp1.append(i)
                        sentences_b.append(temp1)
                    flag = True
                    
            print('preparing forward backward windows...')
            
            sentences,next_chars = [],[]
            sentences.extend(sentences_f)
            sentences.extend(sentences_b)
            next_chars.extend(next_chars_f)
            next_chars.extend(next_chars_b)
            
            X_data = []
            for i in sentences:
                temp = []
                for j in i:
                    temp.append(word_to_index[j])
                X_data.append(temp)  
                
            y_data=[]
            for i in next_chars:
                y_data.append(self.char_indices[i])
            #y_train = np_utils.to_categorical(y_data, vocab_size)
            y_train = np.zeros((len(sentences), self.vocab_size), dtype=np.bool)
            #X_train = sequence.pad_sequences(X_data, maxlen=maxlen)
            
            for i in range(len(y_data)):
                y_train[i][y_data[i]] = True
            
            self.X_data = X_data
            self.y_data = y_train

    def train(self,data):
        print 'building model.....'
        self.prepare_data(data,re_train=True)
        inputs = Input(shape=(self.step,),dtype='int32')
        embed = Embedding(self.vocab_size,self.embedding_dims,input_length=self.step)(inputs)
        encode = LSTM(128)(embed)
        pred = Dense(self.vocab_size,activation='softmax')(encode)
        model = Model(input=inputs,output=pred)
        model.compile(loss='categorical_crossentropy',
                      optimizer='adam',
                      metrics=['accuracy'])
        history = LossHistory()
        model.fit(self.X_data, self.y_data,
                  batch_size=self.batch_size,
                  nb_epoch=self.nb_epoch,callbacks=[history])
        #self.avg_loss = loss.history['loss']
        self.history = history
        with open('history','wb') as h:
            pickle.dump(history.losses,h)
        
        model_json = model.to_json()
        with open("model.json", "w") as json_file:
            json_file.write(model_json)
        # serialize weights to HDF5
        model.save_weights("model.h5")
    
    def prediction(self,model,inp_sent):
        
        voc = {}
        for i in self.vocab:
            voc[i[0]] = 1
        t = []
        for i in inp_sent:
            try:
                w = voc[i]
                t.append(i)
            except:
                t.append(self.unk_token)
        inp_sent = t
        temp = [self.START for i in range(self.step)]
        x_data = []
        for word in inp_sent:
            temp.remove(temp[0])
            temp.append(word)
            if word!=self.END:
                temp1 = []
                for i in temp:
                    temp1.append(i)
                x_data.append(temp1)
        X_big = []
        for i in x_data:
            temp = []
            for j in i:
                temp.append(self.char_indices[j])
            X_big.append(temp)   
        pred1 = []
        for i in X_big:
            data = np.matrix(i)
            pred1.append(self.indices_char[model.predict(data).argmax()])
        temp = [self.END for i in range(self.step)]
        x_data = []
        for word in inp_sent[::-1]:
            temp.remove(temp[0])
            temp.append(word)
            if word!=self.START:
                temp1 = []
                for i in temp:
                    temp1.append(i)
                x_data.append(temp1)        
        X_big = []
        for i in x_data:
            temp = []
            for j in i:
                temp.append(self.char_indices[j])
            X_big.append(temp)   
        pred2 = []
        for i in X_big:
            data = np.matrix(i)
            pred2.append(self.indices_char[model.predict(data).argmax()])
            
        return [pred1,pred2]
        
    def compute_cost(self,model,inp_sent):
        
        if len(inp_sent)<2:
            with open('history','rb')as h:
                loss = pickle.loads(h.read())
            avg_loss = (max(loss)+min(loss))/2
            return avg_loss
        voc = {}
        for i in self.vocab:
            voc[i[0]] = 1
        t = []
        for i in inp_sent:
            try:
                w = voc[i]
                t.append(i)
            except:
                t.append(self.unk_token)
        inp_sent = t
        temp = [self.START for i in range(self.step)]
        count = len(inp_sent)-2
        for i in range(len(temp)-1,-1,-1):
            temp[i] = inp_sent[count]
            count -= 1
            if count == -1:
                break
        x_data=[]
        #print '1st ',temp
        y_vec = np.zeros((1, self.vocab_size), dtype=np.bool)
    
        for i in temp:
            x_data.append(self.char_indices[i])
    
        y_vec[0, self.char_indices[inp_sent[-1]]] = 1
        x_data = np.matrix(x_data)
        y_vec = np.matrix(y_vec)
        cost1 = model.test_on_batch(x_data,y_vec)[0]
        for i in inp_sent:
            if i==self.unk_token:
                cost1+=self.rho
    
        temp = [self.END for i in range(self.step)]
        count = len(inp_sent)-2
        inp_sent.reverse()
        for i in range(len(temp)-1,-1,-1):
            temp[i] = inp_sent[count]
            count -= 1
            if count == -1:
                break
        x_data=[]
        y_vec = np.zeros((1, self.vocab_size), dtype=np.bool)
        #print 'here ',temp
        #print '2 ',inp_sent
        for i in temp:
            x_data.append(self.char_indices[i])
    
        y_vec[0, self.char_indices[inp_sent[-1]]] = 1
        x_data = np.matrix(x_data)
        y_vec = np.matrix(y_vec)
        cost2 = model.test_on_batch(x_data,y_vec)[0]
        for i in inp_sent:
            if i==self.unk_token:
                cost2+=self.rho
        inp_sent.reverse()
        #print 'query ',' '.join(inp_sent),'***** forward cost  : ',cost1,' backward cost : ',cost2
        return (float(cost1)+float(cost2))/2
        
