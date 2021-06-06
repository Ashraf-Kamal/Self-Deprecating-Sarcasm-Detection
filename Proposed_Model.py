import tensorflow as tf
tf.logging.set_verbosity(tf.logging.ERROR)
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from keras.models import Model
from keras.layers import Dense, Flatten, LSTM, Conv1D, MaxPooling1D, Dropout, Activation, Input, Embedding, Bidirectional, TimeDistributed, merge, concatenate, GRU
from keras.optimizers import RMSprop
from keras.preprocessing.text import Tokenizer
from keras.preprocessing import sequence
from keras.callbacks import EarlyStopping
import keras_metrics
import keras.backend as K
from keras.models import Sequential
import os
from keras.layers import Layer
import Attention_Class as Attention

'''
This python is implemented in Python 3.5 to implement the proposed model by applying deep learning techniques in Keras. It takes candidate self-referential tweet 
as the input and forwarded it to the embedding layer. Further, convolutional layer in the proposed model is used to extracts self-deprecating sarcasm-based syntactic
and semantic features from the pre-trained GloVe embedding vectors, and Bi-directional Gated Recurrent Unit (BiGRU) is considered to capture both the preceding and 
succeeding self-deprecating sarcasm-based contextual sequences. However, BiGRU in the proposed model is constituted using two custom GRUs, wherein one of the GRU 
moves in the succeeding directions (i.e., left to right of a self-referential tweet) to capture contextual information based succeeding sequences, and another GRU 
moves in the preceding directions (i.e., right to left of a self-referential tweet) to capture contextual information-based preceding sequences using the parameter 
'go_backwards=True'.

In the proposed model, two attention layers are used, wherein using one attention layer, succeeding context is obtained from the succeeding contextual sequences 
extracted from the forward hidden layer of BiGRU, whereas using another attention layer, preceding context is obtained from the preceding contextual sequences 
extracted from the backward hidden layer of BiGRU for a candidate self-referential tweet. Thereafter, the outcome of both attention layers are concatenated together
to obtain a comprehensive context representation. Finally, the sigmoid is applied to classify the processed that comprehensive contextual representation. 
As a result, a self-referential tweet is classified as either self-deprecating sarcasm (SDS) or non-self-deprecating sarcasm (NSDS).

'''

import random as rn
os.environ['PYTHONHASHSEED'] = '0'
np.random.seed(37)
rn.seed(1254)
tf.set_random_seed(89)
from keras import backend as K
session_conf = tf.ConfigProto(
      intra_op_parallelism_threads=1,
      inter_op_parallelism_threads=1)

sess = tf.Session(graph=tf.get_default_graph(), config=session_conf)
K.set_session(sess)

def recall_m(y_true, y_pred):
        true_positives = K.sum(K.round(K.clip(y_true * y_pred, 0, 1)))
        possible_positives = K.sum(K.round(K.clip(y_true, 0, 1)))
        recall = true_positives / (possible_positives + K.epsilon())
        return recall

def precision_m(y_true, y_pred):
        true_positives = K.sum(K.round(K.clip(y_true * y_pred, 0, 1)))
        predicted_positives = K.sum(K.round(K.clip(y_pred, 0, 1)))
        precision = true_positives / (predicted_positives + K.epsilon())
        return precision

def f1_m(y_true, y_pred):
    precision = precision_m(y_true, y_pred)
    recall = recall_m(y_true, y_pred)
    return 2*((precision*recall)/(precision+recall+K.epsilon()))

def main():
        
    # All seven Datasets which are used for self-deprecating sarcasm detection task.
    
    df = pd.read_csv(r'Final_Data_Sets\Ptacek_Annotated\Ptacek_Manual_Balanced.csv',delimiter=',',encoding='latin-1')
    #df = pd.read_csv(r'Final_Data_Sets\Sem_Eval_Annotated\SEM_EVAL_Manual_Balanced.csv',delimiter=',',encoding='latin-1')
    #df = pd.read_csv(r'Final_Data_Sets\Riloff_Annotated\Riloff_Manual_Balanced.csv',delimiter=',',encoding='latin-1')
    #df = pd.read_csv(r'Final_Data_Sets\Bamman\Bamman_Balanced.csv',delimiter=',',encoding='latin-1')
    #df = pd.read_csv(r'Final_Data_Sets\Ghosh\Ghosh_Balanced.csv',delimiter=',',encoding='latin')
    #df = pd.read_csv(r'Final_Data_Sets\Ling\Ling_Balanced.csv',delimiter=',',encoding='latin-1')
    #df = pd.read_csv(r'Final_Data_Sets\Twitter\Twitter_Balanced.csv',delimiter=',',encoding='latin')

    df=df.dropna()

    X = df.Tweet
    Y = df.Label
    le = LabelEncoder()
    Y = le.fit_transform(Y)
    Y = Y.reshape(-1,1)
    X_train,X_test,Y_train,Y_test = train_test_split(X, Y,test_size=0.2, random_state = 42)

    max_words =8000
    max_len = 20
    tok = Tokenizer(num_words=max_words)

    tok.fit_on_texts(X_train)
    sequences = tok.texts_to_sequences(X_train)
    print (sequences)
    sequences_matrix = sequence.pad_sequences(sequences,maxlen=max_len)
    print (sequences_matrix)

    tok.fit_on_texts(X_test)
    sequences = tok.texts_to_sequences(X_test)
    print (sequences)
    X_test = sequence.pad_sequences(sequences,maxlen=max_len)
    print (X_test)

    embeddings_index = dict()
    f = open('Glove\glove.twitter.27B.200d.txt',encoding="utf8")
    for line in f:    
        values = line.split()
        word = values[0]
        coefs = np.asarray(values[1:], dtype='float32')
        embeddings_index[word] = coefs
    print (len(embeddings_index))
    f.close()
    embedding_matrix = np.zeros((max_words, 200))
    for word, index in tok.word_index.items():
        if index > max_words - 1:
            break
        else:
            embedding_vector = embeddings_index.get(word)
            if embedding_vector is not None:
                embedding_matrix[index] = embedding_vector
    #print (embedding_matrix)

    input_1 = Input(shape=(20,), name='input')
    embedding=Embedding(max_words, 200, input_length=max_len, weights=[embedding_matrix], trainable=False)(input_1)
    CNN=Conv1D(256, 3, activation='relu')(embedding)
    Max_Pool=MaxPooling1D(pool_size=2)(CNN)

    '''
    Below, the first GRU moves in the succeeding directions (i.e., left to right direction of a self-referential tweet) to capture the contextual information based 
    succeeding sequences, and it is fed to the attention layer, wherein succeeding context for self-deprecating sarcasm words/tokens is obtained from the succeeding 
    sequences extracted from the forward hidden layer of the GRU.
    '''

    GRU1= GRU(256, return_sequences=True)(Max_Pool)
    GRU1_Drop = Dropout(0.4)(GRU1)
    atten_1= Attention.attention()(GRU1_Drop)

    '''
    Below, the second GRU moves in the preceding directions (i.e., right to left direction of a self-referential tweet) using the parameter 'go_backwards=True' to 
    capture the contextual information based preceding sequences, and it is fed to the attention layer, wherein preceding context for self-deprecating sarcasm 
    words/tokens is obtained from the preceding sequences extracted from the backward hidden layer of the GRU.
    '''

    GRU2= GRU(256, return_sequences=True, go_backwards=True)(Max_Pool)
    GRU2_Drop = Dropout(0.4)(GRU2)
    atten_2= Attention.attention()(GRU2_Drop)

    merged = concatenate([atten_1, atten_2])
    Final_output = Dense(1, activation="sigmoid", trainable=True)(merged)
    model = Model(inputs=[input_1], outputs=Final_output)
    model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['acc', precision_m, recall_m, f1_m])
    model.summary()
    #es = EarlyStopping(monitor='val_loss', mode='min', verbose=1)   
    #hist =model.fit(sequences_matrix,Y_train, validation_data=(X_test, Y_test), batch_size=256, epochs=100, verbose=2, callbacks=[es])
    hist =model.fit(sequences_matrix,Y_train, validation_data=(X_test, Y_test), batch_size=256, epochs=100, verbose=2)
    accr = model.evaluate(X_test, Y_test, verbose=0)
    print('Testing set\n  Loss: {:0.3f}\n  Accuracy: {:0.3f} \n  Precision: {:0.3f} \n  Recall: {:0.3f} \n  F-score: {:0.3f}'.format(accr[0],accr[1],accr[2],accr[3],accr[4]))
		
    print (np.mean(hist.history['loss']))
    print (np.mean(hist.history['acc']))
    print (np.mean(hist.history['precision_m']))
    print (np.mean(hist.history['recall_m']))
    print (np.mean(hist.history['f1_m']))
    
    print (np.mean(hist.history['val_loss']))
    print (np.mean(hist.history['val_acc']))
    print (np.mean(hist.history['val_precision_m']))
    print (np.mean(hist.history['val_recall_m']))
    print (np.mean(hist.history['val_f1_m']))

    #Saved model results in Model_Save folder.
    
    model.save('Model_Save\Proposed_Model_Ptacek')
    #model.save('Model_Save\Proposed_Model_SemEval')
    #model.save('Model_Save\Proposed_Model_Riloff')
    #model.save('Model_Save\Proposed_Model_Bamman')
    #model.save('Model_Save\Proposed_Model_Ghosh')
    #model.save('Model_Save\Proposed_Model_Ling')
    #model.save('Model_Save\Proposed_Model_Twitter_280')

if __name__ == '__main__':
    main()


