import os
os.environ["TF_CPP_MIN_LOG_LEVEL"]="3"
import sys
import csv
import nltk
from nltk.corpus import stopwords 
from nltk.tokenize import word_tokenize
from ast import literal_eval as make_tuple
import pandas as pd
'''
This program is implemented in Python 2.7, and it merges all the identified implicit self-referential tweets
and the set of explicit self-referential tweets to generate a final dataset of candidate self-referential tweets.
'''

stop_words = list(set(stopwords.words('english')))
stop_words=map(str, stop_words)
stop_words=[]
stop_words.extend(['i', 'am', 'me', 'myself', 'mine', 'my', 'im', 'we', 'us', 'are' , 'our', 'ourselves' ,'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l','m', 'm', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x','y', 'z']) 

df = pd.read_csv('Filtered_Data_Sets\Twitter-280\Merge\Sarcasm_Cluster_Instance.csv', skipfooter=1)
df.to_csv('Filtered_Data_Sets\Twitter-280\Merge\Sarcasm_Cluster_Instance.csv')

def jaccard_Sim(a, b):
	try:		
		c = a.intersection(b)
		return float(len(c)) / (len(a) + len(b) - len(c))    	
	except:
		print('An error occurred in jaccard_Similarity.') 

try:	
	Matched_cluster=[]	
	with open('Filtered_Data_Sets\Twitter-280\Merge\Sarcasm_Pattern_Cluster_list.csv', 'rb') as f:
		reader = csv.reader(f)
		Cluster_list = list(reader)
	print Cluster_list	
	flat_list = [item for sublist in Cluster_list for item in sublist]
	#print flat_list
	Pattern_words = set([make_tuple(x.strip()) for x in flat_list])	
	print Pattern_words

	with open('Filtered_Data_Sets\Twitter-280\Implicit\Sarcasm_Twitter-280.csv', 'rb') as f:
		reader = csv.reader(f)
		Tweet_Implicit_list = list(reader)		
	
	for i in Tweet_Implicit_list:		
		Implict_text= ', '.join(map(str, i))						
		text_list = nltk.word_tokenize(Implict_text) 
		word_tokens = [word for word in text_list if word.isalpha()]
		filtered_sentence = [w for w in word_tokens if not w in stop_words]
		Implicit_texts_words = set(nltk.ngrams(filtered_sentence, n=3))				
		Jacard_score=jaccard_Sim(Implicit_texts_words,Pattern_words)				
		if Jacard_score>0.6:
			print Jacard_score			
			Matched_cluster.append(i)
			print Matched_cluster	
	file_exists = os.path.isfile('Filtered_Data_Sets\Twitter-280\Explicit\Sarcasm_Filtered_Implicit_tweets.csv')
	csvFile = open('Filtered_Data_Sets\Twitter-280\Explicit\Sarcasm_Filtered_Implicit_tweets.csv', 'w')
	writer = csv.writer(csvFile, lineterminator='\n')
	writer.writerows(Matched_cluster)	

except:
	print('An error occurred in Clustring Process.')









	
