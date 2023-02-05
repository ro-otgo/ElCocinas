"""
Este script se encarga de extraer los ingredientes de los ficheros de texto.
Se deben configurar las siguientes variables:

VIDEO_TXT_DIR : Variable que se encarga de almacenar la ruta donde se encuentran
 los ficheros a procesar.
INGREDIENTS_TXT_FILE: Fichero donde se encuentran los ingredientes
OUTPUT_DIR: Directorio en el que se volcaran los resultados de la ejecucion. 
 Se mantiene la mismas estructura de carpetas que la presente en VIDEO_TXT_DIR.

"""
import nltk
from nltk.corpus import stopwords, words
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
import spacy
from spacy.matcher import Matcher

from datetime import datetime
import time
import os

__author__ = 'ro-otgo'

VIDEO_TXT_DIR = r'output_transcripciones\processed'
INGREDIENTS_TXT_FILE = r'ETL\Codigo\ingredients\dataset_ingredients\ingredientes_espanol\ingredientes-processed-es.txt'
OUTPUT_DIR = r'output_transcripciones\ingredientes\es\processed\spacy'

wnl = WordNetLemmatizer()
excluded = ['ingredients']
nlp = spacy.load("en_core_web_sm")
nlp = spacy.load("es_core_news_sm")
nlp = spacy.load("es_core_news_sm", disable=['parser','ner'])
lemmatizer = nlp.get_pipe("lemmatizer")
matcher = Matcher(nlp.vocab)
pattern = [{"POS": "NOUN"}]
matcher.add("nouns_pattern", [pattern])
matcherCebolla =  Matcher(nlp.vocab)
patternCebolla = [{"TEXT": "cebolla"}]
matcherCebolla.add("cebolla", [patternCebolla])


def extract_nouns(file_text: str)-> set:
    # Word validation:
    #   - Word Lemmatize: ['wine', 'juice', 'broiler', 'rooster', 'corn', 'beef', 'pepper', 'pumpkin', 'hand', 'curry', 'cream', 'meat', 'chocolate', 'salt', 'spinach', 'bacon', 'cheese', 'sugar']
    #   - No Lemmatize: ['wine', 'corn', 'sugar', 'spinach', 'juice', 'bacon', 'chips', 'pepper', 'cheese', 'beef', 'broiler', 'curry', 'pumpkin', 'cream', 'crackers', 'salt', 'meat']
    # No validation, no lemmatize:
    #   ['salsa', 'artichokes', 'pumpkin', 'olives', 'bacon', 'pepper', 'crackers', 'juice', 'salt', 'Velveeta', 'beef', 'meat', 'chips', 'cream', 'onions', 'corn', 'sugar', 'cheese', 'wine', 'spinach', 'broiler', 'curry']
    stop_words = set(stopwords.words('spanish'))
    with open (file_text, 'r+',encoding='utf-8') as file:
        text = file.read()
        sent_text = nltk.sent_tokenize(text)
        nouns = set()
        for sentence in sent_text:
            word_tokens = word_tokenize(sentence)
            filtered_sentence_list = [wnl.lemmatize(w) for w in word_tokens]
            # filtered_sentence_list = [wnl.lemmatize(w) for w in word_tokens if not w.lower() in stop_words]
            for (word,pos) in nltk.pos_tag(filtered_sentence_list):
                if pos[0] =='N' and word in words.words() and word.lower() not in stop_words:
                # if pos[0] =='N':
                    nouns.add(word)
    return nouns

def extract_nouns_no_lemmatize(file_path: str)-> set:
    # Word validation:
    #   - Word Lemmatize: ['wine', 'juice', 'broiler', 'rooster', 'corn', 'beef', 'pepper', 'pumpkin', 'hand', 'curry', 'cream', 'meat', 'chocolate', 'salt', 'spinach', 'bacon', 'cheese', 'sugar']
    #   - No Lemmatize: ['wine', 'corn', 'sugar', 'spinach', 'juice', 'bacon', 'chips', 'pepper', 'cheese', 'beef', 'broiler', 'curry', 'pumpkin', 'cream', 'crackers', 'salt', 'meat']
    # No validation, no lemmatize:
    #   ['salsa', 'artichokes', 'pumpkin', 'olives', 'bacon', 'pepper', 'crackers', 'juice', 'salt', 'Velveeta', 'beef', 'meat', 'chips', 'cream', 'onions', 'corn', 'sugar', 'cheese', 'wine', 'spinach', 'broiler', 'curry']
    stop_words = set(stopwords.words('spanish'))
    with open (file_path, 'r+',encoding='utf-8') as file:
        text = file.read()
        sent_text = nltk.sent_tokenize(text)
        nouns = set()
        for sentence in sent_text:
            word_tokens = word_tokenize(sentence)
            filtered_sentence_list = [w for w in word_tokens]
            # filtered_sentence_list = [wnl.lemmatize(w) for w in word_tokens if not w.lower() in stop_words]
            for (word,pos) in nltk.pos_tag(filtered_sentence_list):
                if pos[0] =='N' and word in words.words() and word.lower() not in stop_words:
                # if pos[0] =='N':
                    nouns.add(word)
    return nouns

def read_ingredients(ingredient_path: str)-> set:
    with open(ingredient_path,'r+') as file:
        data = file.readlines()
        data[:] = [wnl.lemmatize(line.strip()) for line in data]
        return set(data)


def __test_nltk():
    ingredients_set = read_ingredients(INGREDIENTS_TXT_FILE)
    print("########")
    init_time = time.time()
    nouns_set = extract_nouns(r'Scraping\Datos\processed\primeros\video__KwZPgxQnmc.txt')
    end_time = time.time()
    print('NLTK:',str(end_time-init_time))
    result = ingredients_set.intersection(nouns_set)
    print(list(result))
    print("########")

def write_ingredients(ingredients:set , parent_folder: str, file_name: str)-> None:
    if not os.path.exists(os.path.join(OUTPUT_DIR, parent_folder)):
        # os.mkdir(os.path.join(OUTPUT_DIR,parent_folder))
        os.makedirs(os.path.join(OUTPUT_DIR,parent_folder))

    with open( os.path.join(OUTPUT_DIR, parent_folder, file_name), 'w+', encoding='utf-8') as file:
        file.writelines('\n'.join(ingredients))

def spacy_extract_nouns(file_text: str)-> set:
    with open (file_text, 'r+',encoding='utf-8') as file:
        text = file.read()
        text_doc = nlp(text)
        matches = matcher(text_doc)
        cebolla_matches = matcherCebolla(text_doc)
        stopword_es = nltk.corpus.stopwords.words('spanish')
        nouns = set()
        for _, start, end in matches:
            token = text_doc[start:end]
            if token.lemma_ not in stopword_es:
                nouns.add(token.lemma_)
        return nouns

def __read_ingredients_spacy(ingredient_path: str)-> set:
    with open(ingredient_path,'r+') as file:
        text = file.read()
        text_doc = nlp(text)
        data = [token.lemma_ for token in text_doc]
        return set(data)

def __test_spacy():
    init_time = time.time()
    nouns_set = spacy_extract_nouns(r'output_transcripciones\processed\output_transcripciones\video_QtP_hQGaDzU.txt')
    end_time = time.time()
    ingredients_set = read_ingredients(INGREDIENTS_TXT_FILE)
    result = ingredients_set.intersection(nouns_set)
    print(list(result))

import sys
def __test_spacy_es():
    text_doc = nlp('En mi casa hay cebollas')
    for token in text_doc:
        print(token, token.lemma_, token.tag_, token.is_stop)
    print("#"*10)
    text_1 = 'que le damos a la coccion conseguimos todos sus jugos sin iniciar tomate cebolla aceite'
    text_doc = nlp(text_1)
    for token in text_doc:
        print(token, token.lemma_, token.tag_, token.is_stop)
    print("-"*20)
    for word in text_1.split(' '):
        print(word)
        text_doc = nlp(word)
        for token in text_doc:
            print(token, token.lemma_, token.tag_, token.is_stop)

if __name__ == '__main__':
    # print(nlp('cebolla')[0].lemma_)
    # __test_spacy_es()
    # __test_spacy()
    # __test_nltk()
    # if True:
        # sys.exit()
    ingredients_set = read_ingredients(INGREDIENTS_TXT_FILE)
    time_data = []
    for root, dirs, files in os.walk(VIDEO_TXT_DIR, topdown=True):
        dirs[:] =  [d for d in dirs if d not in excluded]
        for file in files:
            if file.endswith('txt'):
                nouns_set = spacy_extract_nouns(os.path.join(root,file))
                result = ingredients_set.intersection(nouns_set)
                write_ingredients(result, os.path.basename(root), file)
                time_data.append('{time_data}: {file_name}'.format(time_data=datetime.now().strftime('%d-%m-%Y %H:%M:%S'), file_name=file))

    with open('timelog_spacy_es.txt','w+',encoding='utf-8') as file:
        file.writelines('\n'.join(time_data))
