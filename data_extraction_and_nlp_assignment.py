# -*- coding: utf-8 -*-
"""Data Extraction and NLP_assignment.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1C-UAqVAX-lZo1Qrf_Quc3x8tVvOAO5P6
"""

from google.colab import drive
drive.mount('/content/drive')

import os
ROOT = "/content/drive/MyDrive/BlackCoffer"
os.chdir(ROOT)

import pandas as pd
import numpy as np

# Using Selenium to extract contents from the websites
!pip install selenium
from selenium.webdriver.chrome.service import Service
!pip install webdriver_manager

# We will use BeautifulSoup to read the html contents

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import codecs
import re
from webdriver_manager.chrome import ChromeDriverManager
#from selenium.webdriver.chrome.service import Service

!apt-get update 
!apt install chromium-chromedriver

from selenium import webdriver
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')
driver = webdriver.Chrome('chromedriver',chrome_options=chrome_options)
#driver=webdriver.Chrome(service=Service(ChromeDriverManager().install()))

!pwd

with open('Input.xlsx', 'rb') as f:
        data = pd.read_excel(f)
data

# function to get the source of the webpage
def get_page_source(web):
  wait = WebDriverWait(driver, 10)
  driver.get(web)
  get_url = driver.current_url
  wait.until(EC.url_to_be(web))


  if get_url == web:
    page_source = driver.page_source
    return page_source

# function to get texr from the webpage
def get_text(page_source):
  soup = BeautifulSoup(page_source,"html.parser")

  text = soup.find_all('p')

  return text

# function to filter out the unwanted text from the text
def preprocess_content(text):
  content = []
  paras = len(text)
  for i in range(paras):
    soup2 = BeautifulSoup(str(text[i]), 'html.parser')
    content.append(re.sub('\xa0', '', soup2.get_text()))
  return content

# Create a directory for the article files if it doesn't already exist
def create_directory():
  if not os.path.exists("articles"):
      os.makedirs("articles")

# Save the article text to a file
def save_text_file(text,content,article_id):
  paras = len(text)
  if not os.path.exists(f"articles/{article_id}.txt"):
    with open(f"articles/{article_id}.txt", "w") as f:
      for i in range(paras):
        f.write(content[i])

from typing_extensions import dataclass_transform
def run_processes():
  for index, row in data.iterrows():
    # Access data for each column by column name
    article_id = data['URL_ID'][index]
    WEB =data['URL'][index]
    page_source = get_page_source(WEB)
    text = get_text(page_source)
    content = preprocess_content(text)
    create_directory()
    save_text_file(text,content,article_id)

run_processes()

"""**TEXT ANALYSIS**"""

os.listdir()

#!unzip StopWords-20221226T201449Z-001.zip

#!unzip MasterDictionary-20221226T201605Z-001.zip

os.chdir('/content/drive/MyDrive/BlackCoffer')

os.chdir('StopWords')
stopwords_type = os.listdir()
stopwords_type

import chardet
stop_words = []
for i in stopwords_type:
  #print('start')
  with open(i , "rb") as f:
    contents = f.read()
    encoding = chardet.detect(contents)["encoding"]
  with open(i , "r", encoding = encoding) as f:
    l =   f.read().split()
  stop_words = stop_words+l
stop_words

# nltk
import nltk
from nltk.corpus import stopwords
from  nltk.stem import SnowballStemmer
import re

nltk.download('stopwords')
stopwords = stopwords.words("english")
stopwords

print(len(stopwords))
print(len(stop_words))
stopwords = stopwords + stop_words
print(len(stopwords))

CLEAN_TEXT = "@\S+|https?:\S+|http?:\S|[^A-Za-z0-9]+"
stemmer = SnowballStemmer("english")
def preprocess(text, stem=False):
    # Remove link,user and special characters
    text = re.sub(CLEAN_TEXT, ' ', str(text).lower()).strip()
    filtered_words = [word for word in text.split() if word.lower() not in stopwords]
    tokens = []
    for token in filtered_words:
        if token not in stopwords:
            if stem:
                tokens.append(stemmer.stem(token))
            else:
                tokens.append(token)
    return " ".join(tokens)

os.chdir('/content/drive/MyDrive/BlackCoffer/articles')

# read content from the text file
def read_para(text_file):
  with open( text_file, "rb") as f:
   contents = f.read()
  return contents

# get contents of each text file in the form of dictionary
def get_contents():
  os.chdir('/content/drive/MyDrive/BlackCoffer/articles')
  contents = {}
  for i in range(len(os.listdir())):
    contents[i] = read_para(os.listdir()[i])
    contents[i]  = str(contents[i] )
    contents[i] = contents[i].replace('\\xe2', ' ')
    contents[i]  = contents[i].replace('\\x80', ' ')
    contents[i]  = contents[i].replace('\\x99', ' ')
    contents[i]  = contents[i].replace('\\xa6', ' ')
    contents[i]  = contents[i].replace('\\x93', ' ')
    contents[i] = preprocess(contents[i])

    i+=1

  return contents

# number of words in in text file in the form of a list
def number_of_words(contents):
  os.chdir('/content/drive/MyDrive/BlackCoffer/articles')
  num_words = []
  for i in range(len(os.listdir())):
    k = contents[i].split()
    num_words.append(len(k))
    i+=1
   
  return num_words

# number of personal pronouns in each text file in the form of a list
def personal_pronouns():
  os.chdir('/content/drive/MyDrive/BlackCoffer/articles')
  contents = {}
  num_personal_pronouns=[]
  for i in range(len(os.listdir())):
    contents[i] = read_para(os.listdir()[i])
    contents[i] = str(contents[i])
    q = len([element for element in contents[i].split() if element in ["I","you"  ,                                                                                      "you" ,
                                                                                        "he" ,"she",
                                                                                        "it", "we", 
                                                                                        "they", 
                                                                                        "them", 
                                                                                        "us", 
                                                                                        "him", 
                                                                                        "her", 
                                                                                        "his", 
                                                                                        "hers", 
                                                                                        "its", 
                                                                                        "theirs", 
                                                                                        "our", "your"]])
    num_personal_pronouns.append(q)
    i+=1
  return num_personal_pronouns

# number of sentences in each text file in the form of a list
def num_sentences():
  os.chdir('/content/drive/MyDrive/BlackCoffer/articles')
  contents = {}
  num_sentences =[]
  for i in range(len(os.listdir())):
    contents[i] = read_para(os.listdir()[i])
    contents[i] = str(contents[i]) 
    sentences = contents[i].split('. ') 
    sentences = [sentences[j] for j in range(len(sentences))]   
    num_sentences.append(len(sentences))

    i+=1

  return num_sentences

# read text file linewise
def read_text(filename):
    with open(filename, 'rb') as f:
        contents = f.readlines()
        #words = contents.split('\n')
    return contents

# extract the list of positive and negative words from the master dictionary
def words_type():
  path = '/content/drive/MyDrive/BlackCoffer/MasterDictionary'
  os.chdir(path)
  positive_words, negative_words = read_text(os.listdir()[0]),read_text(os.listdir()[1])
  positive_words = [str(positive_words[i])[2:-3] for i in range(len(positive_words))]
  negative_words = [str(negative_words[i])[2:-3] for i in range(len(negative_words))]
  return positive_words,negative_words

positive_words, negative_words = words_type()

"""## **Calculating Scores**"""

# calculate positive and negative score of all articles, return in the form of a list
def score(list1, contents):
  score = []
  for i in range(len(contents)):
    common_elements =[]
    current = contents[i].split()
    common_elements= [element for element in list1 if element in current]
  
    score.append(len(common_elements))
    i+=1

  return score

def get_positive_score(contents):
  positive_words, negative_words = words_type()
  positive_score = score(positive_words, contents)
  return positive_score

def get_negative_score(contents):
  positive_words, negative_words = words_type()
  negative_score = score(negative_words, contents)
  return negative_score

# polarity scores of all articles int he form of text
def polarity(positive_score, negative_score):
  os.chdir('/content/drive/MyDrive/BlackCoffer/articles')
  polarity = []
  for i in range(len(os.listdir())):
    polarity.append((positive_score[i]-negative_score[i])/((positive_score[i]+negative_score[i]) + .000001))
    i+=1
  
  return polarity

# average sentence length of each text file in the form of a list
def avg_sentence_length(num_words, num_sentence):

  os.chdir('/content/drive/MyDrive/BlackCoffer/articles')
  avg_sent_len = []
  for i in range(len(os.listdir())):

    avg_sent_len.append(num_words[i]/num_sentence[i])

    i+=1 
  return avg_sent_len

# subjectivity of each article
def subjectivity (positive_score, negative_score,number_of_words):
  subjectivity = []
  os.chdir('/content/drive/MyDrive/BlackCoffer/articles')
  for i in range(len(os.listdir())):
    subjectivity.append((positive_score[i] + negative_score[i])/ (number_of_words[i] + 0.000001))

    i+=1

  return subjectivity

# calculate number of syllables in each word
def count_syllables(word):
  syllables = [element for element in [word[i] for i in range(len(word))] if element in ['a','e','i','o','u'] ]
  number_of_syllables = len(syllables)
  try:

    if word[-1] == 'e':
      number_of_syllables = number_of_syllables -1

    if word[-2:] == 'le' or word[-3:]=='les':
      if word[-3] not in ['a','e','i','o','u']:
        number_of_syllables = number_of_syllables + 1

    if word[-2:] == 'es' or 'ed':
      number_of_syllables = number_of_syllables -1
  
  except Exception as e:
    pass
   


  return len(syllables)

# count number of complex words in each article
def count_complex_words(contents):
  complex_word_count={}
  os.chdir('/content/drive/MyDrive/BlackCoffer/articles')
  for i in range(len(contents)):
      complex_word_count[i] = 0
      for word in contents[i].split():
          if count_syllables(word) > 2:
              complex_word_count[i] += 1
      i+=1
  
  return complex_word_count

#percentage of complex words   
def complex_percentage(number_of_complex_words,number_of_words):
  percent_complex =[]

  os.chdir('/content/drive/MyDrive/BlackCoffer/articles')
  for i in range(len(os.listdir())):
    try:
      percent_complex.append((number_of_complex_words[i]/number_of_words[i])*100)
    except Exception as e:
      percent_complex.append(0)

    i+=1
  
  return percent_complex

# fog index of each article
def fog_index(avg_sentence_length,percent_complex):
  Fog_Index =[]
  os.chdir('/content/drive/MyDrive/BlackCoffer/articles')

  for i in range(len(os.listdir())):
    p = 0.4 * (avg_sentence_length[i] + percent_complex[i])
    Fog_Index.append(p)
    i+=1
  
  return Fog_Index

# number of syllable per word
def syllable_per_word(contents, number):
  syllable_per_word=[]

  for i in range(len(number)) :
    count = 0
    current = contents[i].split()
    for j in range(len(current)):
      syl = count_syllables(current[j])
      count= count+syl
      j+=1
    try:
      syllable_per_word.append(count/number[i])
    except Exception as e:
      syllable_per_word.append('0')     
    i+=1

  return syllable_per_word

# average word length of each article
def avg_word_length(contents, number):
  avg_word_len=[]
  for i in range(len(number)):
    count = 0
    current = contents[i].split()
    for j in range(len(current)):
     count = count + len(current[j])
     j+=1
    try:
     avg_word_len.append(count/number[i])
    except Exception as e:
      avg_word_len.append('0') 
    i += 1

  return avg_word_len

"""### **CREATE THE OUTPUT FOLDER**"""

def create_output_directory():
  if not os.path.exists("Output"):
      os.makedirs("Output")

output_frame = pd.DataFrame(columns = ['URL_ID', 'URL', 'POSITIVE SCORE',
                                       'NEGATIVE SCORE','POLARITY SCORE',
                                       'SUBJECTIVITY SCORE','AVG SENTENCE LENGTH','PERCENTAGE OF COMPLEX WORDS',
                                       'FOG INDEX','AVG NUMBER OF WORDS PER SENTENCE','COMPLEX WORD COUNT',
                                       'WORD COUNT','SYLLABLE PER WORD','PERSONAL PRONOUNS','AVG WORD LENGTH'])

output_frame

def fill_url_info():
  ids = list(data['URL_ID'])
  urls = list(data['URL'])
  output_frame['URL_ID'] = ids
  output_frame['URL'] = urls
  return output_frame

fill_url_info()

def fill_score():
  contents = get_contents()
  l1=get_positive_score(contents)
  output_frame['POSITIVE SCORE'] = l1
  l2 =get_negative_score(contents)
  output_frame['NEGATIVE SCORE'] = l2
  output_frame['POLARITY SCORE'] = polarity(l1,l2)
  w = number_of_words(contents)
  s = num_sentences()
  output_frame['WORD COUNT'] = w
  output_frame['SUBJECTIVITY SCORE'] = subjectivity(l1,l2,w)
  output_frame['SYLLABLE PER WORD']= syllable_per_word(contents,w)
  output_frame['AVG WORD LENGTH'] = avg_word_length(contents, w)
  output_frame['AVG SENTENCE LENGTH'] = avg_sentence_length(w,s)
  output_frame['AVG NUMBER OF WORDS PER SENTENCE'] = output_frame['WORD COUNT']/s

fill_score()

output_frame

def fill_complex_scores():
  contents = get_contents()
  w = number_of_words(contents)
  c = list(count_complex_words(contents).values())
  pc = complex_percentage(c,w)
  output_frame['COMPLEX WORD COUNT'] = c
  output_frame['PERCENTAGE OF COMPLEX WORDS'] = complex_percentage(c,w)
  output_frame['FOG INDEX'] = fog_index(output_frame['AVG SENTENCE LENGTH'],pc)
  output_frame['PERSONAL PRONOUNS'] =personal_pronouns()

fill_complex_scores()

type(contents.values())

output_frame

#save the output data in the form of an excel file

os.chdir('/content/drive/MyDrive/BlackCoffer/')

create_output_directory()

os.chdir('Output')

output_frame.to_excel('output.xlsx', index=False)

