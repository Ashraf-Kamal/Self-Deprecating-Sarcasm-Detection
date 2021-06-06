import enchant
import nltk
from nltk.corpus import stopwords 
from nltk.tokenize import word_tokenize 
import csv
import pandas as pd
import os

#This program is implemented in Python 2.7. In this program, all tweets containing less than three tokens/words are filtered out from further consideration.


lst_filtered_tweet=[]
df = pd.read_csv('Pre_Processed_Data_Sets\Preprocess_1\Twitter-280\Sarcasm_Twitter-280.csv')
df=df.dropna()
cnt=0
for index, row in df.iterrows():
	if (len(row['Tweet_Text'].split())>3):		
		cnt +=1
		print cnt		
		lst_filtered_tweet.append([row['Tweet_Text'],row['Tweet_Id']])

lst_filtered_tweet.insert(0, ['Tweet','Tweet_Id'])		
		
file_exists = os.path.isfile('Pre_Processed_Data_Sets\Preprocess_2\Twitter-280\Sarcasm_Twitter-280.csv')
csvFile = open('Pre_Processed_Data_Sets\Preprocess_2\Twitter-280\Sarcasm_Twitter-280.csv', 'w')
writer = csv.writer(csvFile, lineterminator='\n')
writer.writerows(lst_filtered_tweet)


