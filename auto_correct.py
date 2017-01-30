# -*- coding: utf-8 -*-
from  code_run import Aggarwal, Kothari, Soundex_class, concat_error
from learning_model import dllm
import pickle, itertools
from keras.models import model_from_json

class auto_correct:
    
    def __init__(self,data=False,re_train=False,vocab_size=10000,step=6,batch_size=128,nb_epoch=10,embed_dims=200):
        self.dllm = dllm(vocab_size,step,batch_size,nb_epoch,embed_dims)
        self.dictionary = {}
        self.misp = []
        self.phn = []
        self.concat = []
        self.cor = []
        self.al_queries = []
        
        if re_train == True:
            self.dllm.train(data)
            for i in self.dllm.vocab:
                if len(i[0])>1:
                    self.dictionary[i[0]]=1
            self.dictionary['a']=1
            self.dictionary['i']=1
            self.dictionary['u']=1
            self.dictionary['s']=1
        else:
            self.dllm.prepare_data(data,re_train)
            #a=open('new_words.txt').readlines()
            #a=open('new_coca1.txt').readlines()
            #a=[i.split('\r')[0]for i in a]
            #for i in a:
            #    self.dictionary[i] = 1
            for i in self.dllm.vocab:
                if len(i[0])>1:
                    self.dictionary[i[0]]=1
            self.dictionary['a']=1
            self.dictionary['i']=1
            self.dictionary['u']=1
            self.dictionary['s']=1

            #with open('coc_dump')as h:
            #   self.dictionary = pickle.loads(h.read())
        #a=open('new_coca1.txt').readlines()
        json_file = open('model.json', 'r')
        loaded_model_json = json_file.read()
        json_file.close()
        self.model = model_from_json(loaded_model_json)
        with open('history')as h:
            history = pickle.loads(h.read())
        avg_cost = (max(history)+min(history))/2
        self.avg_loss = avg_cost + (max(history)-avg_cost)/2
        # load weights into new model
        self.model.load_weights("model.h5")
        self.model.compile(loss='categorical_crossentropy',
                      optimizer='adam',
                      metrics=['accuracy'])
        self.words_expansion = []
    
    def char_check(self,ch,misp):
        for i in range(0,len(misp)):
            if misp[i] not in ch:
                return False
            if misp.count(misp[i]) != ch.count(misp[i]):
                return False
        return True
        
    def valid_range(self,ch,misp):
        if len(ch)>len(misp)-2 and len(ch)<len(misp)+3:
            return True
        else:
            return False
    
    def is_string(self,ch):
        try:
            a=int(ch)
            return False
        except:
            return True
            
    def check_split(self,sent1):
        sent = []
        flag = False
        for i in sent1:
            sent.append(i)
        for i in range(len(sent)-1): 
            try:
                w = self.dictionary[sent[i]+sent[i+1]] 
                sent[i] = sent[i]+sent[i+1]
                sent.remove(sent[i+1])
                flag = True
                i=i+1
            except:
                #words.append(sent[i])
                continue
        if len(sent)>1 and flag:
            cost = self.dllm.compute_cost(self.model,sent)
        else:
            cost = 5
        return sent,cost
        
    def run(self,words=False,ind=False):
        inp_words=words
        if words == False:
            words = raw_input('enter the query\n').lower()
        #print words
        words = words.split()
        mini = []
        obj = concat_error()
        words[0] = obj.learn_few(words[0])        
        #print 'final text ',' '.join(words)
        self.words_expansion = []
        concat_words = []
        count = 0
        pos=[]
        phonetic_flag = True
        
        #print words
        if len(words)>1:
            cost = self.dllm.compute_cost(self.model,words)
            cost_split = self.check_split(words)   
            if cost > cost_split[1]:
                words = cost_split[0]
        #print words
        
        for i in words:
            try:
                count+=1
                w=self.dictionary[i]
            except:
                obj = concat_error()
                temp = obj.wordBreak(i,self.dictionary.keys())
                #print 'here',temp
                if len(temp)>0:
                    phonetic_flag = False
                    pos.append(count-1)
                    for sent in temp:
                        concat_words.append(tuple(sent.split()))
                continue
        #print concat_words,pos
        if len(concat_words)>0:
            self.concat.append((words,ind))
            for sent in concat_words:
                cost = {}
                min_cost=100
                cost[sent] = self.dllm.compute_cost(self.model,sent)
                if cost[sent]<min_cost:
                    mini.append(sent)
                    min_cost = cost[sent]
            #print mini
            new_sent = []
            k=0
            for i in range(len(words)):
                #print i,k
                if i==pos[k]:
                    new_sent.extend(list(mini[k]))
                    if k+1 < len(pos):
                        k+=1
                else:
                    new_sent.append(words[i])
            #print new_sent
        else:
            new_sent = words
        if len(new_sent)<2:
            try:
                w=self.dictionary[words[0]]
                #print words
                self.cor.append((words,ind))
            except:
                obj = Soundex_class(words[0],self.dictionary.keys(),1)
                self.misp.append((words,ind))
                w=obj.run()
                self.cor.append((w,ind))
                #print w
            return
            
        for i in new_sent:
            #print 'at - ',i
            if len(i)<2:
                continue
            try:
                w = self.dictionary[i]
                #w = run(i)[0]
                self.words_expansion.append([i])
            except:
                self.misp.append((new_sent,ind))
                phonetic_flag = False
                obj = Kothari(i,self.dictionary.keys(),10)
                words_kothari = obj.cal()
                obj = Soundex_class(i,self.dictionary.keys(),5)
                words_soundex = obj.run()
                obj = Aggarwal(i,self.dictionary.keys(),5)
                words_agg = obj.cal()
                w1 = []
                #print words_kothari
                #print words_agg
                #print words_soundex
                alpha,beta,gamma = 4,3,3
                for j in words_kothari:
                    if len(w1)<alpha:
                        if self.char_check(j,i) and self.valid_range(j,i):
                            w1.append(j)
                            if j in words_agg:
                                words_agg.remove(j)
                            if j in words_soundex:
                                words_soundex.remove(j)
                    if len(w1)==alpha:
                        break
                #print words_soundex
                #print words_agg
                #print 'final words ',w1
                for j in words_soundex:
                    if len(w1)-alpha<beta:
                        if self.char_check(j,i) and self.valid_range(j,i):
                            w1.append(j)            
                            if j in words_agg:
                                words_agg.remove(j)
                    if len(w1)==alpha+beta:
                        break
                for j in words_agg:
                    if len(w1)-alpha-beta<gamma and self.char_check(j,i) and self.valid_range(j,i):
                        w1.append(j)
                if len(w1) == 0:
                    w1.append(words_kothari[0])
                    if len(words_soundex)>1:
                        w1.append(words_soundex[0])
                self.words_expansion.append(w1)
                
        if phonetic_flag == True:
            #print new_sent
            self.words_expansion = []
            cost = self.dllm.compute_cost(self.model,new_sent)
            #cost_split = self.check_split(new_sent)   
            #print cost,cost_split
            if cost > self.avg_loss:
                #print 'phonetic error possibility ::'
                self.phn.append((new_sent,ind))
                self.words_expansion.append([new_sent[0]])
                for i in new_sent[1:]:
                    if len(i) > 2 and self.is_string(i):
                        obj = Soundex_class(i,self.dictionary.keys(),3)
                        words = obj.run()
                        for j in words:
                            if len(j)<2:
                                words.remove(j)
                        if len(words)>0:
                            if i not in words:
                                words[-1]=i
                            self.words_expansion.append(words)
                        else:
                            self.words_expansion.append([i])
                    else:
                        self.words_expansion.append([i])
            else:
                self.words_expansion = [[i] for i in new_sent]
        
        queries = list(itertools.product(*self.words_expansion))
        queries = list(set(queries))
        self.all_queries = queries
        #print 'number of queries formed', len(queries) 
        #bre            
        mini = [100,0]
        cost = {}
        #print queries
        #print new_sent
        #print words
        for i in queries:
            cost[i] = self.dllm.compute_cost(self.model,i)
            if cost[i]<mini[0]:
                mini[0] = cost[i]
                mini[1] = i
        try:
            if inp_words == False:
                print ' '.join(mini[1]),'  ',mini[0]
            else:
                c =' '.join(mini[1]),mini[0]
                self.cor.append((c,inp_words,ind))
            #print ' '.join(mini[1]),'  ',mini[0]
        except:
            print new_sent
            print 'invalid input'
        #print wrong1,mini