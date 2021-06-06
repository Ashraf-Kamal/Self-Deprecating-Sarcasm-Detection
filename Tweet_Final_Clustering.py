import os
os.environ["TF_CPP_MIN_LOG_LEVEL"]="3"
import sys
import csv

'''
This program is implemented in Python 2.7 to retain only those explicit self-referential tweets
cluster file which consists of at least three explicit self-referential tweets.
'''

try:	
	with open('Filtered_Data_Sets\Twitter-280\Merge\Sarcasm_DFS_Clustering.csv', 'rb') as f:
	    reader = csv.reader(f)
	    Cluster_list = list(reader)
	#print Cluster_list
	Final_tri_gram_cluster=[]
	Final_Cluster_list = [map(int, x) for x in Cluster_list]
	print Final_Cluster_list

	for x in Final_Cluster_list:
	    if len(x)>=3:
	    	print x
	    	Final_tri_gram_cluster.append(x)

	print Final_tri_gram_cluster
	file_exists = os.path.isfile('Filtered_Data_Sets\Twitter-280\Merge\Sarcasm_Final_DFS_Clusters.csv')
	csvFile = open('Filtered_Data_Sets\Twitter-280\Merge\Sarcasm_Final_DFS_Clusters.csv', 'w')
	writer = csv.writer(csvFile, lineterminator='\n')
	writer.writerows(Final_tri_gram_cluster)	

except:
	print('An error occurred in Clustring Process.')
