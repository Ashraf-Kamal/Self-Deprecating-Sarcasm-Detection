from __future__ import absolute_import
import warnings
warnings.filterwarnings("ignore")
import csv
import os
import nltk
import math
from nltk.corpus import stopwords 
from nltk.tokenize import word_tokenize

'''
This program is implemented in Python 2.7. After the identification of clusters from explicit self-referential tweets, 
frequent patterns from the obtained clusters are mined. In the end, a unique set of frequent patterns is filtered from 
frequent patterns set by removing the duplicate frequent patterns.
'''

stop_words = list(set(stopwords.words('english')))
stop_words=map(str, stop_words)
stop_words=[]
stop_words.extend(['i', 'am', 'me', 'myself', 'mine', 'my', 'im', 'we', 'our', 'us', 'ourselves', 'are', 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l','m', 'm', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x','y', 'z']) 

try:
    with open('Filtered_Data_Sets\Twitter-280\Merge\Sarcasm_Final_DFS_Clusters.csv', 'rb') as f:
        reader = csv.reader(f)
        Filtered_Cluster_list = list(reader)   
    Final_Filtered_cluster=[]
    Final_Filtered_cluster = [map(int, x) for x in Filtered_Cluster_list]
    print Final_Filtered_cluster
except:
    print('An error occurred in Final_DFS_Cluster Process.')

file_exists = os.path.isfile('Filtered_Data_Sets\Twitter-280\Merge\Sarcasm_Cluster_Instance.csv')
csvFile = open('Filtered_Data_Sets\Twitter-280\Merge\Sarcasm_Cluster_Instance.csv', 'ab')
fields = ('Tweet_Id','Tweet_Text') #field names
csvWriter = csv.writer(csvFile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
csvWriter = csv.DictWriter(csvFile, fieldnames=fields)
if file_exists:
   csvWriter.writeheader()

def cluster_temp(j):
    print j
    with open('Filtered_Data_Sets\Twitter-280\Explicit\Sarcasm_Twitter-280.csv') as csvDataFile:
        data = [row for row in csv.reader(csvDataFile)]    	
    	return data[j-1][0]

Cluster_no=1
s=1
tri_gram_cluster=[]
Final_tri_gram_cluster=[]
try:
    csvWriter.writerow({'Tweet_Id': 0, 'Tweet_Text': 'Cluster: ' + str(Cluster_no)})
    for i in Final_Filtered_cluster:	
        for j in i:
            print s,j,i
            text=cluster_temp(j)
            print text
            text_list = nltk.word_tokenize(text)            
            word_tokens = [word for word in text_list if word.isalpha()]
            filtered_sentence = [w for w in word_tokens if not w in stop_words]
            words = set(nltk.ngrams(filtered_sentence, n=3))
            tri_gram_cluster.append(words)
            csvWriter.writerow({'Tweet_Id': s, 'Tweet_Text': text})            
            s=s+1
                            
        print
        Cluster_no=Cluster_no+1        
        
        flat_list = [item for sublist in tri_gram_cluster for item in sublist]    
        s=s-1
        s=s*0.5        
        s=int(math.floor(s))        
        print sorted(set([i for i in flat_list if flat_list.count(i)]))
        print len(sorted(set([i for i in flat_list if flat_list.count(i)])))
        Final_tri_gram_cluster.append(sorted(set([i for i in flat_list if flat_list.count(i)>=s])))        
        tri_gram_cluster=[]
        csvWriter.writerow({'Tweet_Id': 0, 'Tweet_Text': 'Cluster: ' + str(Cluster_no)})
        s=1    
    Final_tri_gram_cluster = filter(None, Final_tri_gram_cluster)
    print Final_tri_gram_cluster

except:
    print ('An error occurred in cluster-tweets-filteration process.')

file_exists = os.path.isfile('Filtered_Data_Sets\Twitter-280\Merge\Sarcasm_Pattern_Cluster_list.csv')
csvFile = open('Filtered_Data_Sets\Twitter-280\Merge\Sarcasm_Pattern_Cluster_list.csv', 'w')
writer = csv.writer(csvFile, lineterminator='\n')
writer.writerows(Final_tri_gram_cluster)

