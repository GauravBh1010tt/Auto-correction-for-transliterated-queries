#!/usr/bin/env python2
# -*- coding: utf-8 -*-

import pickle, itertools
from  code_run import Kothari

class bigram_auto:
    
    def __init__(self):
        self.bi_gram = {}
        self.vocab = {}
        self.words_expansion = []
        self.queries = []

    def create_bigram(self,data=False,num_of_ques=False):
        
        if data==False:
            with open('Eng_queries_20K','rb')as h:
                data = pickle.loads(h.read())
        if num_of_ques:
            data = data[0:num_of_ques]
    
        for i in data:
            if len(i)>1:
                for j in range(0,len(i)-2):
                    try:
                        self.bi_gram[(i[j],i[j+1])]+=1
                    except:
                        self.bi_gram[(i[j],i[j+1])] = 1
        
        for i in data:
            for j in i:
                if len(j)>0:
                    self.vocab[j]=1
    
    def model(self,data=False,num_of_ques=False):
        self.create_bigram(data=False,num_of_ques=False)
        query = raw_input('enter the query\n')
        #words_expansion=[]
        #queries = []
        for i in query.split():
            try:
                w = self.vocab[i]
                self.words_expansion.append([i])  
                #print 'here'
            except:
                #print 'there'
                obj = Kothari(i,self.vocab.keys(),5)
                subs_words = obj.cal()
                #print 'now',subs_words
                self.words_expansion.append(subs_words)
        #print 'here',words_expansion
        self.queries = list(itertools.product(*self.words_expansion))
        self.queries = list(set(self.queries))
        prev_score = -1
        count = 0
        for i in self.queries:
            score = 0
            for j in range(0,len(i)-2):
                try:
                    score+=self.bi_gram[(i[j],i[j+1])]
                except:
                    continue
            if score > prev_score:
                prev_score = score
                item = count
            count+=1
        print ' '.join(self.queries[item])
        #return words_expansion, queries