# -*- coding: utf-8 -*-
from __future__ import absolute_import
from pattern.en import suggest
from collections import Counter
import tweepy
import os
import sys
import string
import re
import pickle
import preprocessor as p
import numpy as np
import nltk
from collections import Counter
from nltk import tokenize
import HTMLParser
import unicodedata2
import itertools
from nltk.corpus import wordnet
from textblob import TextBlob

#This program is implemented in Python 2.7. In this program, various unwanted and undesirable information is eliminated from tweets
#to produce better results. It consists of several pre-processed steps, such as removal of symbols, punctuation marks,
#URL's, retweets, mentions, ampersands, dots, white spaces, double quotes, emoticons, and numbers, and convert into lower case. 

p.set_options(p.OPT.MENTION)
Whitespace = re.compile(u"[\s\u0020\u00a0\u1680\u180e\u202f\u205f\u3000\u2000-\u200a]+", re.UNICODE)

# This method is for extracting contraction.
def Expand_Contractions(text):
    text = text.replace(" can't ", ' cannot ').replace("can't've ", ' cannot have ').replace("'cause ", ' because ').replace("ain't ", ' am not ')\
        .replace("could've ", ' could have ').replace("couldn't ", ' could not ').replace("couldn't've ", ' could not have ')\
        .replace("doesn't ", ' does not ').replace("don't ", ' do not ').replace("hadn't ", ' had not ').replace("hadn't've ", ' had not have ') \
        .replace("hasn't ", ' has not ').replace("haven't ", ' have not ').replace("he'd ", ' he would ').replace("he'd've ", ' he would have ') \
        .replace("he'll ", ' he will ').replace("he'll've ", ' he will have ').replace("he's ", ' he is ').replace("how'd ", ' how did ') \
        .replace("how'd'y ", ' how do you ').replace("how'll ", ' how will ').replace("how's ", ' how is ').replace("I'd ", ' I would ') \
        .replace("I'd've ", ' I would have ').replace("I'll ", ' I will ').replace("I'll've ", ' I will have ').replace("I'm ", ' I am ') \
        .replace("I've ", ' I have ').replace("isn't ", ' is not ').replace("it'd ", ' it had ').replace("it'd've ", ' it would have ') \
        .replace("it'll ", ' it will ').replace("it'll've ", ' it will have ').replace("it's ", ' it is ').replace("let's ", ' let us ') \
        .replace("ma'am ", ' madam ').replace("mayn't ", ' may not ').replace("might've ", ' might have ').replace("mightn't ", ' might not ') \
        .replace("mightn't've ", ' might not have ').replace("must've ", ' must have ').replace("might've ", ' might have ') \
        .replace("mustn't've ", ' must not have ').replace("needn't ", ' need not ').replace("needn't've ", ' need not have ') \
        .replace("oughtn't", ' ought not ').replace("oughtn't've ", ' ought not have').replace("shan't ", ' shall not ')\
        .replace("shan't've", ' shall not have ').replace("sha'n't've ", ' shall not have').replace("she'd ", ' she would ')\
        .replace("mustn't ", ' must not ').replace("aren't ", ' are not ').replace("o'clock ", ' of the clock ').replace("sha'n't ", ' shall not ') \
        .replace("she'd've ", ' she would have ').replace("she'd've ", ' she would have ').replace("o'clock ", ' of the clock ') \
        .replace("sha'n't ", ' shall not ').replace("she'll ", ' she will ').replace("she'll've ", ' she will have ').replace("she's ", ' she is ')\
        .replace("should've ", ' should have ').replace("shouldn't ", ' should not ').replace("shouldn't've ", ' should not have ')\
        .replace("so've ", ' so have ').replace("didn't ", ' did not ').replace("so's ", ' so is ').replace("that'd ", ' that would ')\
        .replace("that'd've ", ' that would have ').replace("that's ", ' that is ').replace("there'd ", ' there had ').replace("there's ", ' there is ')\
        .replace("there'd've ", ' there would have ').replace("they'd ", ' they would ').replace("they'd've ", ' they would have ')\
        .replace("they'll ", ' they will ').replace("they'll've ", ' they will have ').replace("they're ", ' they are ').replace("they've ", ' they have ')\
        .replace("to've ", ' to have ').replace("wasn't ", ' was not ').replace("we'd ", ' we had ').replace("we'd've ", ' we would have ')\
        .replace("we'll ", ' we will ').replace("we'll've ", ' we will have ').replace("we're ", ' we are ').replace("we've ", ' we have ')\
        .replace("weren't ", ' were not ').replace("what'll ", ' what will ').replace("what'll've ", ' what will have').replace("what're ", ' what are ')\
        .replace("what's ", ' what is ').replace("what've ", ' what have ').replace("when's ", ' when is').replace("when've ", ' when have ')\
        .replace("where'd ", ' where did ').replace("where's ", ' where is ').replace("where've ", ' where have').replace("who'll ", ' who will ')\
        .replace("who'll've ", ' who will have ').replace("who's ", ' who is ').replace("who've ", ' who have').replace("why's ", ' why is ')\
        .replace("why've ", ' why have ').replace("will've ", ' will have ').replace("won't ", ' will not ').replace("won't've ", ' will not have ')\
        .replace("would've ", ' would have ').replace("wouldn't ", ' would not ').replace("wouldn't've ", ' would not have').replace("'s ",' is ')\
        .replace("y'all ", ' you all ').replace("y'alls ", ' you alls ').replace("y'all'd ", ' you all would').replace("y'all'd've ", ' you all would have ')\
        .replace("y'all're ", ' you all are ').replace("y'all've ", ' you all have ').replace("you'd ", ' you had').replace("you'd've ", ' you would have ')\
        .replace("you'll ", ' you will ').replace("you'll've ", ' you will have ').replace("you're ", ' you are').replace("you've ", ' you have')\
        .replace("cant ", ' cannot').replace("i'm", ' i am').replace("im", ' i am').replace("can t ", ' cannot').replace("mayt ", ' maynot')    
    return text;

# This method is for removing URL.
def Strip_Links(text):
    link_regex    = re.compile('((https?):((//)|(\\\\))+([\w\d:#@%/;$()~_?\+-=\\\.&](#!)?)*)', re.DOTALL)
    links         = re.findall(link_regex, text)
    for link in links:
        text = text.replace(link[0], ' ')    
    return text

# Twitter text comes HTML-escaped, so unescape it.
# We also first unescape &amp;'s, in case the text has been buggily double-escaped.
def Remove_Ampersand(text):
    text = text.replace("&amp;", "&")
    text = HTMLParser.HTMLParser().unescape(text)
    return text

# "am   I  " => "am I"
# Remove White Spaces
def Remove_Extra_Whitespace(tweet):
    #return re.sub( '\s+', ' ', input).strip()
    #return Whitespace.sub(" ", input).strip()
    s=' '.join(tweet.split())
    return s

# This function is to convert lower case letter
def Convert_Lowercase(preprocessed_tweet):
    return preprocessed_tweet.lower()

# This function is to convert upper case letter
def Convert_Uppercase(preprocessed_tweet):
    return preprocessed_tweet.upper()    

# This function is to convert Camel case letter
def Convert_Camelcase(preprocessed_tweet):
    return preprocessed_tweet.title()

# This function is to remove hex care
def Remove_Hexchar(preprocessed_tweet):
    return preprocessed_tweet.decode('utf8').encode('ascii', errors='ignore')

# This function is to remove AT_USER
def Remove_Retweets(tweet):
	return re.sub('@[^\s]+','AT_USER',tweet)


def ReplaceTwoOrMore(s):
    pattern = re.compile(r"(.)\1{1,}", re.DOTALL)    
    return  pattern.sub(r"\1\1", s)
    
def Remove_charaters(tweet):
    #Convert @username with space
    tweet=re.sub('\ |\,|\`|\\|\/|\&|\*|\'|\;|\(|\)|\:|\/|\=|\-|\%|\$', ' ', tweet)    
    tweet = re.sub(r'#[a-zA-Z0-9]*', '', tweet)
    return tweet  

def Remove_Retweets(tweet):
	tweet=re.sub(r'\bRT\b', '', tweet)
	return tweet

# Strip space, " and ' from tweet
def Remove_Quotes(tweet):
	tweet = tweet.strip(' "\'')	
	# Remove - & 'tweet = re.sub(r'(-|\')', '', tweet)
	return tweet

def Remove_Emojis(tweet):
    # Smile -- :), : ), :-), (:, ( :, (-:, :')
    tweet = re.sub(r'(:\s?\)|:-\)|\(\s?:|\(-:|:\'\))', ' ', tweet)
    # Laugh -- :D, : D, :-D, xD, x-D, XD, X-D
    tweet = re.sub(r'(:\s?D|:-D|x-?D|X-?D)', ' ', tweet)
    # Love -- <3, :*
    tweet = re.sub(r'(<3|:\*)', ' ', tweet)
    # Wink -- ;-), ;), ;-D, ;D, (;,  (-;
    tweet = re.sub(r'(;-?\)|;-?D|\(-?;)', ' ', tweet)
    # Sad -- :-(, : (, :(, ):, )-:
    tweet = re.sub(r'(:\s?\(|:-\(|\)\s?:|\)-:)', ' ', tweet)
    # Cry -- :,(, :'(, :"(
    tweet = re.sub(r'(:,\(|:\'\(|:"\()', ' ', tweet)
    return tweet

def Remove_Numbers(tweet):
    tweet = re.sub(r'[0-9]+', '', tweet)
    return tweet

def Remove_Capital_Words(tweet):
    tweet = re.sub(r'\b[A-Z]+\b', '', tweet)
    return tweet

def Remove_All_Dots(tweet):
    tweet = re.sub(r'(?<!\d)\.(?!\d)', ' ', tweet)
    tweet = Remove_Extra_Whitespace(tweet)
    return tweet

def Preprocessing_Start(raw_tweet):
    preprocessed_tweet=  Expand_Contractions(raw_tweet)    
    preprocessed_tweet = p.clean(Strip_Links(preprocessed_tweet))        
    preprocessed_tweet = Remove_Ampersand(preprocessed_tweet)  # This function removes ampersand (&amp) in raw tweets.    
    preprocessed_tweet = Remove_Hexchar(preprocessed_tweet)  # This function removes hexa char in raw tweets.      
    preprocessed_tweet = ReplaceTwoOrMore(preprocessed_tweet)  # This function removes two or more white spaces in raw tweets.  
    preprocessed_tweet = Remove_Retweets(preprocessed_tweet)  # This function removes retweets in raw tweets.        
    preprocessed_tweet = Remove_Emojis(preprocessed_tweet) # This function removes emojis in raw tweets.
    preprocessed_tweet = Remove_Quotes(preprocessed_tweet) # This function removes quotes in raw tweets.    
    preprocessed_tweet = Remove_Extra_Whitespace(preprocessed_tweet) # This function removes white spaces in raw tweets.
    preprocessed_tweet = Remove_Numbers(preprocessed_tweet) # This function removes white spaces in raw tweets.
    preprocessed_tweet = Convert_Lowercase(preprocessed_tweet)  # This function converts lower case letter in raw tweets.    
    preprocessed_tweet = Remove_All_Dots(preprocessed_tweet)
     
    return preprocessed_tweet







