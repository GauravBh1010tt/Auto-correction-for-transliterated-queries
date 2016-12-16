# -*- coding: utf-8 -*-

b=open('Speller Challenge TREC Dataset..txt').readlines()
b=[i.split('\t')for i in b]
for i in range(len(b)):
    b[i][1] = b[i][1].split('\r')[0] 
    
error_query=[]

data = [i[1] for i in b]

for i,k in enumerate(b): 
    flag = True
    for j in k[1:]:
        j=j.split('\r')[0]
        if k[0] == j:
            flag=False
    if flag==True:
        error_query.append((k[0],i))