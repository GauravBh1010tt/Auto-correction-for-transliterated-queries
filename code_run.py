# -*- coding: utf-8 -*-
import re
import pickle
from collections import OrderedDict

class Soundex_class:
    dict1={}
    
    def __init__(self,text,words,K):
        self.text = text
        self.K = K
        self.words = words
        self.dict1 = {}
        
    def make_nltk_dump(self):
        #dict1={}
        for i in self.words:
            s1=self.Soundex(i)
            try:
                self.dict1[s1].append(i)
            except:
                self.dict1[s1]=[i]          
            #to remove silent letter k and p from starting
            if i.startswith("k") or i.startswith("p"):
                str1=list(i)
                l=0
                try:
                    while str1[l]=='k' or str1[l]=='p':
                        str1[l]=''
                        l=l+1
                        str1=''.join(str1)
                    s2=self.Soundex(str1)
                    if s1!=s2:
                        try:
                            self.dict1[s2].append(i)
                        except:
                            self.dict1[s2]=[i]
                except:
                     continue           
            #to remove silent words
            str1=list(i)
            if str1.__contains__('k') or str1.__contains__('d') or str1.__contains__('b') or str1.__contains__('g'):        
                l=0
                length=len(i)
                try:
                    while l<length:
                            if str1[l]=='k' or str1[l]=='d' or str1[l]=='b' or str1[l]=='g':
                                str1[l]=''
                            l=l+1
                    str1=''.join(str1)
                    s3=self.Soundex(str1)
                    if s3!=s1 and s3!=s2:
                        try:
                            self.dict1[s3].append(i)
                        except:
                            self.dict1[s3]=[i]
                except:
                    continue     
        #self.dict1 = dict1
        #with open('nltk_dump','wb') as h:
        #        pickle.dump(dict1,h)
          
    def remove_zeros(self,str):
        final=""
        for k in str:
            if k!='0':
                final+=k
        return self.RemoveDupliChar(final)
       
    def RemoveDupliChar(self,Word):
            NewWord=" "
            index=0
            for char in Word:
                    if char!=NewWord[index]:
                            NewWord += char
                            index += 1
            return (NewWord.strip())
    
    def Soundex(self,word):
        str=""
        l=len(word)
        for j in range(0,l):
            i=word[j]
            if i=='a' or i=='e' or i=='i' or i=='o' or i=='u' or i=='y' or i=='h' or i=='w':
                str+='0'
            elif i=='b' or i=='v' or i=='f' or i=='p':
                str+='1'  
            elif i=='c' or i=='j' or i=='k' or i=='q' or i=='s' or i=='x' or i=='z'or i=='g':
                str+='2'
            elif i=='d' or i=='t':
                str+='3'
            elif i=='l':
                str+='4'
            elif i=='m' or i=='n':
                str+='5'
            elif i=='r':
                str+='6'
            else:
                str+=''
        return self.remove_zeros(str)
         
    def lcs(self,a, b):
        lengths = [[0 for j in range(len(b)+1)] for i in range(len(a)+1)]
        # row 0 and column 0 are initialized to 0 already
        for i, x in enumerate(a):
            for j, y in enumerate(b):
                if x == y:
                    lengths[i+1][j+1] = lengths[i][j] + 1
                else:
                    lengths[i+1][j+1] = max(lengths[i+1][j], lengths[i][j+1])
        # read the substring out from the matrix
        result = ""
        x, y = len(a), len(b)
        while x != 0 and y != 0:
            if lengths[x][y] == lengths[x-1][y]:
                x -= 1
            elif lengths[x][y] == lengths[x][y-1]:
                y -= 1
            else:
                assert a[x-1] == b[y-1]
                result = a[x-1] + result
                x -= 1
                y -= 1
        return (result)    
    
    def remove_vowels(self,s):
        result = re.sub(r'[AEIOU]', '', s, flags=re.IGNORECASE)
        return result
        
    def levenshtein(self,s1, s2):
        if len(s1) < len(s2):
            return self.levenshtein(s2, s1)
    
        # len(s1) >= len(s2)
        if len(s2) == 0:
            return len(s1)
            
        previous_row = range(len(s2) + 1)
        for i, c1 in enumerate(s1):
            current_row = [i + 1]
            for j, c2 in enumerate(s2):
                insertions = previous_row[j + 1] + 1 # j+1 instead of j since previous_row and current_row are one character longer
                deletions = current_row[j] + 1       # than s2
                substitutions = previous_row[j] + (c1 != c2)
                current_row.append(min(insertions, deletions, substitutions))
            previous_row = current_row
        return previous_row[-1]
    
    def run(self):
        try:
            #with open('nltk_dump') as h:
            #    dict1=pickle.loads(h.read())
            self.make_nltk_dump()
            dict1 = self.dict1
            text = self.text
            #print text
            text = re.sub('[^a-z0-9\ \']+', " ", text)
            words = list(text.split())
            token=OrderedDict()
            for tok in words:
                str=list(tok)
                l=0
                length=len(tok)
                while l<length:
                        if str[l]=='1':
                            str[l]='one' #one
                        if str[l]=='2':
                            str[l]='to' #to,too,two
                        if str[l]=='3':
                            str[l]='three' #three
                        if str[l]=='4':
                            str[l]='for' #for
                        if str[l]=='5':
                            str[l]='fiv' #fiv
                        if str[l]=='6':
                            str[l]='six' #six
                        if str[l]=='7':
                            str[l]='sev' #sv
                        if str[l]=='8':
                            str[l]='ate' #ate
                        if str[l]=='9':
                            str[l]='nin' #nin
                        l=l+1
                tok=''.join(str)
                s = self.Soundex(tok)
                for i in dict1[s]:
                    if i=='':
                        continue
                    j=len(self.lcs(i,tok))
                    lcsRatio=float(j*2)/(len(tok)+len(i))
                    #print i," ",tok
                    score=lcsRatio/(self.levenshtein(self.remove_vowels(i),self.remove_vowels(tok))+1)
                    try:
                        token[tok].append((score,i))
                    except:
                        token[tok]=[(score,i)]
                        continue
                    
                #to remove extending ssss or zzzzz
                if tok.endswith("s") or tok.endswith("z"):
                    str=list(tok)
                    l=len(tok)-1
                    while str[l]=='s' or str[l]=='z':
                        str[l]='\0'
                        l=l-1
                    str=''.join(str)        
                    st=self.Soundex(str)
                    if s!=st:
                        for i in dict1[st]:
                            j=len(self.lcs(i,tok))
                            lcsRatio=float(j*2)/(len(tok)+len(i))
                            score=lcsRatio/(self.levenshtein(self.remove_vowels(i),self.remove_vowels(tok))+1)
                            try:
                                token[tok].append((score,i))
                            except:
                                token[tok]=[(score,i)]
                                continue                
            for i in token.keys():
                token[i].reverse()
                token[i].sort()
                token[i].reverse()
        
            t=[]
            for i in token.keys():
                tmp=[]
                count=0
                for j in token[i]:
                    if count==self.K:
                        break
                    tmp.append(j[1])
                    count=count+1
                t.append(tmp)
            t=t[0]
            t = [i[:-1]for i in t]
            return t 
        except:
            return []
        
class Kothari:
    
    def __init__(self,text,words,K):
        self.text = text
        self.K = K
        self.final_dict={}
        self.words=words
        
    def remove_vowels(self,s):
        result = re.sub(r'[AEIOU]', '', s, flags=re.IGNORECASE)
        return result
        
    def removeDupliChar(self,Word):
            NewWord=" "
            index=0
            for char in Word:
                    if char!=NewWord[index]:
                            NewWord += char
                            index += 1
            return NewWord.strip()
    
    def levenshtein(self,s1, s2):
        if len(s1) < len(s2):
            return self.levenshtein(s2, s1)
    
        # len(s1) >= len(s2)
        if len(s2) == 0:
            return len(s1)
    
        previous_row = range(len(s2) + 1)
        for i, c1 in enumerate(s1):
            current_row = [i + 1]
            for j, c2 in enumerate(s2):
                insertions = previous_row[j + 1] + 1 # j+1 instead of j since previous_row and current_row are one character longer
                deletions = current_row[j] + 1       # than s2
                substitutions = previous_row[j] + (c1 != c2)
                current_row.append(min(insertions, deletions, substitutions))
            previous_row = current_row
        
        return previous_row[-1]+1
        
    def lcs(self,a, b):
        lengths = [[0 for j in range(len(b)+1)] for i in range(len(a)+1)]
        # row 0 and column 0 are initialized to 0 already
        for i, x in enumerate(a):
            for j, y in enumerate(b):
                if x == y:
                    lengths[i+1][j+1] = lengths[i][j] + 1
                else:
                    lengths[i+1][j+1] = max(lengths[i+1][j], lengths[i][j+1])
        # read the substring out from the matrix
        result = ""
        x, y = len(a), len(b)
        while x != 0 and y != 0:
            if lengths[x][y] == lengths[x-1][y]:
                x -= 1
            elif lengths[x][y] == lengths[x][y-1]:
                y -= 1
            else:
                assert a[x-1] == b[y-1]
                result = a[x-1] + result
                x -= 1
                y -= 1
        return result
    
    #print len(lcs('start','stuart'))
    
    def lcs_ratio(self,a,b):
        k=0
        j=0
        k=len(self.lcs(a,b))
        j=len(a)
        return float(k)/j

    def char_check(self,ch):
        for i in ch:
            if i not in self.text:
                return False
        return True
        
    def cal(self):
        try:
            text = self.text
            temp=[]
            score_tuple_list=[]
            ip=''
            #ip=removeDupliChar(remove_vowels(str))
            ip=self.remove_vowels(self.removeDupliChar(text))
            
            for i in self.words:
                t=''
                #t=removeDupliChar(remove_vowels(i))
                t=self.remove_vowels(self.removeDupliChar(i))
                gamma=0
                if i[0]!=text[0]:
                    gamma=0
                else:
                    if len(text)==1 or len(i)==1:
                        gamma=float(self.lcs_ratio(text,i))/self.levenshtein(text,i)
                    else:
                        gamma=float(self.lcs_ratio(ip,t))/self.levenshtein(ip,t)
                score_tuple_list.append((gamma,i))
                
            score_tuple_list.sort()
            score_tuple_list.reverse()
            
            counter = 10
            for i in range(0,20):
                if score_tuple_list[i][1] not in temp:
                    temp.append(score_tuple_list[i][1])
                else:
                    counter+=1
            '''final_words=[]
            for i in temp:
                if len(i)<len(self.text)+3 and self.char_check(i):
                    final_words.append(i)'''
            return temp[0:self.K]
        except:
            return []
           

class Aggarwal:
            
    def __init__(self,text,words,K):
        self.text = text
        self.K = K
        self.words = words
        
        with open("dict1","r") as h:
            self.dict1=pickle.loads(h.read())
            
        with open("dict_rev1","r") as h:
            self.dict_rev=pickle.loads(h.read())
        
    def lcs(self,a, b):
        lengths = [[0 for j in range(len(b)+1)] for i in range(len(a)+1)]
        # row 0 and column 0 are initialized to 0 already
        for i, x in enumerate(a):
            for j, y in enumerate(b):
                if x == y:
                    lengths[i+1][j+1] = lengths[i][j] + 1
                else:
                    lengths[i+1][j+1] = max(lengths[i+1][j], lengths[i][j+1])
        # read the substring out from the matrix
        result = ""
        x, y = len(a), len(b)
        while x != 0 and y != 0:
            if lengths[x][y] == lengths[x-1][y]:
                x -= 1
            elif lengths[x][y] == lengths[x][y-1]:
                y -= 1
            else:
                assert a[x-1] == b[y-1]
                result = a[x-1] + result
                x -= 1
                y -= 1
        return result    
        
    
    def cal(self):  
        text = self.text
        pre={}
        suf={}
        tok=''    
        tok=text
        str_rev=''
        str_rev=text[::-1]    
        
        '''-------------- making prefix dictionary --------------'''
        
        if len(text)==1:
            for i in self.dict1:
                if text[0]==i:
                    for j in range(0,len(self.dict1[i])):    
                        temp=''
                        temp=self.dict1[i][j]
                        try:
                            k=0
                            k=len(self.lcs(text,temp))
                            try:
                                pre[k].append(self.dict1[i][j])
                            except:
                                pre[k]=[self.dict1[i][j]]
                                #print dict[i][j]
                        except:
                            continue
        
        else:
            for i in self.dict1:
                if text[0]==i:
                    for j in range(0,len(self.dict1[i])):
                        temp=''
                        temp=self.dict1[i][j]
                        try:
                            if text[1]==temp[1]:
                                k=0
                                k=len(self.lcs(text,temp))
                                try:
                                    pre[k].append(self.dict1[i][j])
                                except:
                                    pre[k]=[self.dict1[i][j]]
                                #print dict[i][j]
                        except:
                            continue
                    
        '''-------------- making suffix dictionary --------------'''
        
        if len(text)==1:
            for i in self.dict_rev:
                if str[0]==i:
                    for j in range(0,len(self.dict_rev[i])):    
                        temp_rev=''
                        temp_rev=self.dict_rev[i][j]
                        try:
                            k=0
                            k=len(self.lcs(text,temp_rev))
                            try:
                                suf[k].append(self.dict_rev[i][j])
                            except:
                                suf[k]=[self.dict_rev[i][j]]
                                #print dict[i][j]
                        except:
                            continue
        
        else:
            for i in self.dict_rev:
                if str_rev[0]==i:
                    for j in range(0,len(self.dict_rev[i])):
                        t=''
                        temp_rev=''
                        temp_rev=self.dict_rev[i][j]
                        t=temp_rev[::-1]
                        try:
                            if str_rev[1]==temp_rev[1]:
                                k=0
                                k=len(self.lcs(str_rev,temp_rev))
                                try:
                                    suf[k].append(t)
                                except:
                                    suf[k]=[t]
                                #print dict[i][j]
                        except:
                            continue
                    
        '''-------------- more declaration and length calculation --------------'''
                    
        max_pre=0
        max_suf=0
        len_max_pre=0
        len_max_suf=0
        
        if len(pre)>0:
            max_pre=max(pre)
            len_max_pre=len(pre[max_pre])
        
        if len(suf)>0:
            max_suf=max(suf)
            len_max_suf=len(suf[max_suf])
            
        temp=[]
        pre_tuple=[]
        suf_tuple=[]
        
        '''-------------- making score based prefix and suffix tuples --------------'''
        
        if len(pre)>0 and max_pre>0:
            temp=pre[max_pre]
            for i in range(0,len_max_pre):
                pre_tuple.append((max_pre*0.25,temp[i]))
            
        temp=[]    
        
        if len(suf)>0 and max_suf>0:
            temp=suf[max_suf]
            for i in range(0,len_max_suf):
                suf_tuple.append((max_suf*0.25,temp[i]))
            
        '''-------------------------------------------------------------------------'''
        
        final=[]
        temp=[]
        
        len_tuple=0
        len_tuple=len(pre_tuple)
        
        if len_tuple>=3:
            for i in range(0,3):
                final.append(pre_tuple[i])
                #print pre_tuple[i][1]
                
        if len_tuple==1:
            final.append(pre_tuple[0])
            #print pre_tuple[0][1]
            
        if len_tuple==2:
            final.append(pre_tuple[0])
            final.append(pre_tuple[1])
            #print pre_tuple[0][1]
            #print pre_tuple[1][1]
            
        #------------------
        
        len_tuple=0
        len_tuple=len(suf_tuple)
            
        if len_tuple>=3:
            for i in range(0,3):
                final.append(suf_tuple[i])
                #print suf_tuple[i][1]
                
        if len_tuple==1:
            final.append(suf_tuple[0])
            #print suf_tuple[0][1]
            
        if len_tuple==2:
            final.append(suf_tuple[0])
            final.append(suf_tuple[1])
            #print suf_tuple[0][1]
            #print suf_tuple[1][1]
     
        token={}
        #fr=open("new_coca1.txt","r")
        #fr = open('all_words.txt','r')
        for i in self.words:
            #j = re.sub('[^a-z\ \']+', " ", j)
            #words = list(j.split())
            #print words
            try:
                j=len(self.lcs(i,tok))
                score=float(j*2)/(len(tok)+len(i))
                #print "(",score,i,")"
                try:
                    token[tok].append((score,i))
                except:
                    token[tok]=[(score,i)]
                    continue
            except:
                continue
            
            
        token[tok].sort()
        token[tok].reverse()
        
        for j in range(0,6):
            try:
                final.append(token[tok][j])
                #print token[tok][j][1]," "
            except:
                continue   
                
        final.sort()
        final.reverse()
        
        for i in range(0,len(final)):
            if final[i][1] not in temp:
                temp.append(final[i][1])
        
        #return final
        return temp[0:self.K]

class concat_error:
    def wordBreak(self, str1, dict1):
        n=len(str1)
        words=[[] for i in range(n)]
        i=n-1
        while 1:
            if i<0:
                break
            if str1[i:n] in dict1:
                words[i].append(n)
            for j in range(i+1,n):
                if words[j] and str1[i:j] in dict1:
                    words[i]+=[j]
            i-=1
        val=[[0]] 
        prefix=[]
        while val:
            new_val=[]
            for i in val:
                if i[-1]==n:
                    temp=[str1[i[k]:i[k+1]] for k in range(len(i)-1)]
                    prefix.append(' '.join(temp))
                else:
                    for k in words[i[-1]]:
                        new_val.append(i+[k])
            val=new_val
        return prefix
    
    def learn_few(self,words):
        if words == 'hw':
            words = 'how'
        elif words == 'wht' or words =='wt':
            words = 'what'
        elif words == 'whn' or words == 'wn':
            words = 'when'
        elif words == 'hs':
            words ='has'
        elif words == 'wch' or words =='whch':
            words = 'which'
        elif words == 'whr':
            words = 'where'
            
        return words
