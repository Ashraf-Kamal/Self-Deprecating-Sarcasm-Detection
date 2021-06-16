import nltk
from openpyxl import load_workbook
from openpyxl.utils import get_column_letter, column_index_from_string
from openpyxl.compat import range
import pandas as pd
import csv
import os
import ast
import itertools
import nltk
from nltk.corpus import stopwords
import numpy as np 
from nltk.tokenize import word_tokenize
'''
This program is implemented in Python 2.7. It computes the Jaccard similarity between two explicit self-referential tweets 
and saved values in a Jaccard matrix file. An adjacency matrix list is generated from the Jaccard matrix, if the Jaccard similarity 
score is greater than 0.6. Thereafter, conncected components of explicit self-referential tweets are obtained in the form of clusters.
'''

stop_words = list(set(stopwords.words('english')))
stop_words=map(str, stop_words)
stop_words=[]
stop_words.extend(['i', 'am', 'me', 'myself', 'mine', 'my', 'im', 'we', 'our', 'us', 'ourselves', 'are', 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l','m', 'm', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x','y', 'z']) 

def jaccard(a, b):
    try:        
        c = a.intersection(b)
        return float(len(c)) / (len(a) + len(b) - len(c))    	
    except:
        print('An error occurred in jaccard.') 

def Input(sent_1,sent_2):
        try:                
                word_tokens_1 = word_tokenize(sent_1)
                word_tokens_2 = word_tokenize(sent_2)
                word_tokens_1 = [word for word in word_tokens_1 if word.isalpha()]
                word_tokens_2 = [word for word in word_tokens_2 if word.isalpha()]

                filtered_sentence_1 = [w for w in word_tokens_1 if not w in stop_words]
                filtered_sentence_2 = [w for w in word_tokens_2 if not w in stop_words]

                words1 = set(nltk.ngrams(filtered_sentence_1, n=3))
                words2 = set(nltk.ngrams(filtered_sentence_2, n=3))
                if(len(words1)>0 and len(words2)>0):                    
                    res=jaccard(words1, words2)                    
                    return res
                else:
                    return 0
        except:                
                print('An error occurred in jaccard.')

Listid1=[]
Tweet_Similarity1=[]
Tag_list=[] 
with open('Filtered_Data_Sets\Twitter-280\Explicit\Sarcasm_Twitter-280.csv', 'r') as my_file: 
    try:
        reader = csv.reader(my_file, quoting=csv.QUOTE_ALL)
        Tag_list = list(reader)
        for i in range(len(Tag_list)):
            Tweet_Similarity=[]
            Listid=[]
            for j in range(len(Tag_list)):
                if (i<j):
                    print i+1,j
                    res=Input(''.join(Tag_list[i]),''.join(Tag_list[j]))
                    if res>0.6:
                        #print res
                        Listid.append(j+1)
                        Tweet_Similarity.append(res)                                
                    else:
                        Tweet_Similarity.append(0) 
                else:
                    Tweet_Similarity.append(0)
            Tweet_Similarity1.append(Tweet_Similarity)
            Listid1.append(Listid)
    except:
        print('An error occurred.')	

for i in range(len(Listid1)):
	Listid1[i].insert(0,i+1)

file_exists = os.path.isfile('Filtered_Data_Sets\Twitter-280\Merge\Sarcasm_Jacard_matrix_List.csv')
csvFile = open('Filtered_Data_Sets\Twitter-280\Merge\Sarcasm_Jacard_matrix_List.csv', 'w')
writer = csv.writer(csvFile, lineterminator='\n')
writer.writerows(Listid1)	

dict = {}
for l2 in Listid1:
    dict[l2[0]] = l2[1:]

print dict

def connected_components(graph):
    seen = set()
    def dfs(v):
        vs = set([v])
        component=[]
        while vs:
            v = vs.pop()
            seen.add(v)
            vs |= set(graph[v]) - seen
            component.append(v)
        return component
    ans=[]
    for v in graph:
        if v not in seen:
            d=dfs(v)
            ans.append(d)
    return ans

file_exists = os.path.isfile('Filtered_Data_Sets\Twitter-280\Merge\Sarcasm_DFS_Clustering.csv')
csvFile = open('Filtered_Data_Sets\Twitter-280\Merge\Sarcasm_DFS_Clustering.csv', 'w')
writer = csv.writer(csvFile, lineterminator='\n')
writer.writerows(connected_components(dict))	

