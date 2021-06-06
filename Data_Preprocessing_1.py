import enchant
import nltk
from nltk.corpus import stopwords 
from nltk.tokenize import word_tokenize 
import csv
import pandas as pd
import os
from openpyxl import load_workbook
from openpyxl.utils import get_column_letter, column_index_from_string
from openpyxl.compat import range

#This program is implemented in Python 2.7. In this program, custom removal of stop wrods is applied. Stop words related to self-refertial instances/tweets
#(e.g., i, we, me, mine, are etc.) are retained in the stop words list.  


Final_English_Sentence=[]
wrd_chk = enchant.Dict("en_US")

stop_words=['hers', 'between', 'yourself', 'but', 'again', 'there', 'about', 'once', 'during', 'out', 'very', 'having', 'with', 'they',
            'own', 'an', 'be', 'some', 'for', 'do', 'its', 'yours', 'such', 'into', 'of', 'most', 'itself', 'other', 'off', 'is', 'or',
            'who', 'as', 'from', 'him', 'each', 'the', 'themselves', 'until', 'below', 'these', 'your', 'his', 'through', 'don', 'nor',
            'were', 'her', 'more', 'himself', 'this', 'down', 'should', 'their', 'above', 'both', 'up', 'to', 'had', 'she', 'all', 'no',
            'at', 'any', 'before', 'them', 'same', 'and', 'been', 'have', 'in', 'will', 'on', 'does', 'yourselves', 'then', 'that', 'because',
            'what', 'over', 'why', 'so', 'can', 'did', 'not', 'now', 'under', 'he', 'you', 'herself', 'has', 'just', 'where', 'too', 'only',
            'which', 'those', 'after', 'few', 'whom', 'if', 'theirs', 'against', 'by', 'doing', 'it', 'how', 'further', 'was', 'here', 'than',
            'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'j', 'k', 'l', 'm', 'm', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'im',
            '?','!','!!','!!!','!!!!']

def Input(tweet_id,tweet_str):
	try:
		english_words=[]
		print tweet_Id
		word_tokens = word_tokenize(tweet_str)
		word_tokens = [word for word in word_tokens if word.isalpha()]
		filtered_tweet = [w for w in word_tokens if not w in stop_words]
		tweet_final=' '.join(map(str, filtered_tweet))
		print tweet_final		
		english_words.append([tweet_id,tweet_final])
		print english_words
		flat_list = [item for sublist in english_words for item in sublist]
		Final_English_Sentence.append(flat_list)
	except:
 		print('An error occurred in Input.')

df = pd.read_csv('Pre_Processed_Data_Sets\Preprocess_CSV\Twitter-280\Sarcasm_Twitter-280.csv')
print df
df=df.dropna()
cnt=0
for index, row in df.iterrows():
	cnt +=1	
	tweet=row['Tweet_Text']	
	tweet_Id=row['Tweet_Id']		
	tweet_str=tweet.replace('!', '').replace('?', ' ').replace('"', ' ')	
	Input(tweet_Id,tweet_str)
Final_English_Sentence.insert(0, ['Tweet_Id','Tweet_Text'])


file_exists = os.path.isfile('Pre_Processed_Data_Sets\Preprocess_1\Twitter-280\Sarcasm_Twitter-280.csv')
csvFile = open('Pre_Processed_Data_Sets\Preprocess_1\Twitter-280\Sarcasm_Twitter-280.csv', 'w')
writer = csv.writer(csvFile, lineterminator='\n')
writer.writerows(Final_English_Sentence)	


