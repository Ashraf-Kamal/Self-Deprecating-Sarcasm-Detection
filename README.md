# Self-Deprecating Sarcasm Detection

Self-deprecating sarcasm is one of the special categories of sarcasm. This repository contains a newly created Twitter-280 dataset and source code files in Python which are used in the proposed approach for self-deprecating sarcasm detection problem. Due to the Twitter policy, only tweet ids and their respective labels are shared for Twitter-280 dataset. A small description of source code files is mentioned below. 

--------------------------------------------------------------------------------------------------------------------------------------
Pre-requisite:
--------------------------------------------------------------------------------------------------------------------------------------
1. Twitter REST API
2. NLTK 
3. Keras 
4. Numpy 
5. spaCy 
6. Python 2.7, 3.5+
7. GloVe
--------------------------------------------------------------------------------------------------------------------------------------
Tweet_Fetch_Id.py
--------------------------------------------------------------------------------------------------------------------------------------
This program is implemented in Python 2.7. In this program, it takes tweet ids as an input for a dataset, and tweets are fetched against tweet ids, respectively using the Twitter REST API.

--------------------------------------------------------------------------------------------------------------------------------------
Data_Crawling_Preproceesing.py
--------------------------------------------------------------------------------------------------------------------------------------
This program is implemented in Python 2.7. It takes tweet as an input to perform data cleaning tasks using the DFS.Prerocessing_Start function. Data pre-processing task is accomplished in below three steps.

--------------------------------------------------------------------------------------------------------------------------------------
Data_Pre-processing.py
--------------------------------------------------------------------------------------------------------------------------------------
This program is implemented in Python 2.7. In this program, various unwanted and undesirable information is eliminated from tweets to produce better results. It consists of several pre-processed steps, such as removal of symbols, punctuation marks, URL's, retweets, mentions, ampersands, dots, white spaces, double quotes, emoticons, and numbers, and convert into lower case. 

--------------------------------------------------------------------------------------------------------------------------------------
Data_Pre-processing1.py
--------------------------------------------------------------------------------------------------------------------------------------
This program is implemented in Python 2.7. In this program, custom removal of stop words is applied. Stop words related to self-referential instances/tweets (e.g., i, we, me, mine, are, etc.) are filtered from the stop words list.  

--------------------------------------------------------------------------------------------------------------------------------------
Data_Pre-processing2.py
--------------------------------------------------------------------------------------------------------------------------------------
This program is implemented in Python 2.7. In this program, all tweets containing less than three tokens/words are filtered out from further consideration.

--------------------------------------------------------------------------------------------------------------------------------------
Data_Filter.py
--------------------------------------------------------------------------------------------------------------------------------------
This program is implemented in Python 2.7. In this program, spaCy, a popular open-source library for advanced NLP tasks in Python is used. It recognizes linguistic markers like punctuation, and it has the ability to split these punctuation tokens from word tokens. Hence, the performance of the POS tagger using spaCy is not affected, if it is applied to cleaned data. Using spaCy, tweets tokenization and POS tagging task are accomplished. Thereafter, explicit self-referential tweets-based 'Specific' and 'Generic' patterns are matched. These patterns are mainly based on either tokens or the sequential order of tags and tokens or vice-versa. 

--------------------------------------------------------------------------------------------------------------------------------------
Tweet_Jacard_similarity.py
--------------------------------------------------------------------------------------------------------------------------------------
This program is implemented in Python 2.7. It computes the Jaccard similarity between two explicit self-referential tweets and saved values in a Jaccard matrix file. An adjacency matrix list is generated from the Jaccard matrix, if the Jaccard similarity score is greater than 0.6. Thereafter, conncected components of explicit self-referential tweets are obtained in the form of clusters.

--------------------------------------------------------------------------------------------------------------------------------------
Tweet_Final_Clustering.py  
--------------------------------------------------------------------------------------------------------------------------------------
This program is implemented in Python 2.7 to retain only those explicit self-referential tweets cluster file which consists of at least three explicit self-referential tweets.

--------------------------------------------------------------------------------------------------------------------------------------
Tweet_Clustering_Pattern.py  
--------------------------------------------------------------------------------------------------------------------------------------
This program is implemented in Python 2.7. After the identification of clusters from explicit self-referential tweets, frequent patterns from the obtained clusters are mined. In the end, a unique set of frequent patterns is filtered from frequent patterns set by removing the duplicate frequent patterns.

------------------------------------------------------------------------------------------------------------------------------------
Tweets_Clustering_Pattern_Matching.py  
--------------------------------------------------------------------------------------------------------------------------------------
This program is implemented in Python 2.7, and it merges all the identified implicit self-referential tweets and the set of explicit self-referential tweets to generate a final dataset of candidate self-referential tweets.

--------------------------------------------------------------------------------------------------------------------------------------
Proposed_Model.py  
-------------------------------------------------------------------------------------------------------------------------------------
This python is implemented in Python 3.5 to implement the proposed model by applying deep learning techniques in Keras. It takes candidate self-referential tweet as the input and forwarded it to the embedding layer. Further, convolutional layer in the proposed model is used to extracts self-deprecating sarcasm-based syntactic and semantic features from the pre-trained GloVe embedding vectors, and Bi-directional Gated Recurrent Unit (BiGRU) is considered to capture both the preceding and succeeding self-deprecating sarcasm-based contextual sequences. However, BiGRU in the proposed model is constituted using two custom GRUs, wherein one of the GRU moves in the succeeding directions (i.e., left to right of a self-referential tweet) to capture contextual information based succeeding sequences, and another GRU moves in the preceding directions (i.e., right to left of a self-referential tweet) to capture contextual information-based preceding sequences using the parameter 'go_backwards=True'. 

In the proposed model, two attention layers are used, wherein using one attention layer, succeeding context is obtained from the succeeding contextual sequences extracted from the forward hidden layer of BiGRU, whereas using another attention layer, preceding context is obtained from the preceding contextual sequences extracted from the backward hidden layer of BiGRU for a candidate self-referential tweet. Thereafter, the outcome of both attention layers are concatenated together to obtain a comprehensive context representation. Finally, the sigmoid is applied to classify the processed that comprehensive contextual representation. As a result, a self-referential tweet is classified as either self-deprecating sarcasm (SDS) or non-self-deprecating sarcasm (NSDS).

--------------------------------------------------------------------------------------------------------------------------------------
Attention_Class.py  
--------------------------------------------------------------------------------------------------------------------------------------
This program is implemented in Python 3.5. This contains the class of attention layer mechanism.

--------------------------------------------------------------------------------------------------------------------------------------
Cite paper: 
--------------------------------------------------------------------------------------------------------------------------------------
Kamal, A., Abulaish, M. CAT-BiGRU: Convolution and Attention with Bi-Directional Gated Recurrent Unit for Self-Deprecating Sarcasm Detection. Cognitive Computation  Cognitive Computation. Jan (2021), pp.1-19. DOI: https://doi.org/10.1007/s12559-021-09821-0








