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
import os
from datetime import datetime

__author__ = 'ro-otgo'

VIDEO_TXT_DIR = r'Scraping\Datos\processed'
INGREDIENTS_TXT_FILE = r'C:\Users\Rodrigo\Downloads\representation-for-ingredients\test.json\ingredients\train.txt'
OUTPUT_DIR = r'Scraping\Codigo\ingredients\processed'

wnl = WordNetLemmatizer()
excluded = ['ingredients']


def extract_nouns(file_text: str)-> set:
    # Word validation:
    #   - Word Lemmatize: ['wine', 'juice', 'broiler', 'rooster', 'corn', 'beef', 'pepper', 'pumpkin', 'hand', 'curry', 'cream', 'meat', 'chocolate', 'salt', 'spinach', 'bacon', 'cheese', 'sugar']
    #   - No Lemmatize: ['wine', 'corn', 'sugar', 'spinach', 'juice', 'bacon', 'chips', 'pepper', 'cheese', 'beef', 'broiler', 'curry', 'pumpkin', 'cream', 'crackers', 'salt', 'meat']
    # No validation, no lemmatize:
    #   ['salsa', 'artichokes', 'pumpkin', 'olives', 'bacon', 'pepper', 'crackers', 'juice', 'salt', 'Velveeta', 'beef', 'meat', 'chips', 'cream', 'onions', 'corn', 'sugar', 'cheese', 'wine', 'spinach', 'broiler', 'curry']
    stop_words = set(stopwords.words('english'))
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

def extract_nouns_fast(file_path: str)-> set:
    # Word validation:
    #   - Word Lemmatize: ['wine', 'juice', 'broiler', 'rooster', 'corn', 'beef', 'pepper', 'pumpkin', 'hand', 'curry', 'cream', 'meat', 'chocolate', 'salt', 'spinach', 'bacon', 'cheese', 'sugar']
    #   - No Lemmatize: ['wine', 'corn', 'sugar', 'spinach', 'juice', 'bacon', 'chips', 'pepper', 'cheese', 'beef', 'broiler', 'curry', 'pumpkin', 'cream', 'crackers', 'salt', 'meat']
    # No validation, no lemmatize:
    #   ['salsa', 'artichokes', 'pumpkin', 'olives', 'bacon', 'pepper', 'crackers', 'juice', 'salt', 'Velveeta', 'beef', 'meat', 'chips', 'cream', 'onions', 'corn', 'sugar', 'cheese', 'wine', 'spinach', 'broiler', 'curry']
    stop_words = set(stopwords.words('english'))
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


def __test():
    ingredients_set = read_ingredients(r'C:\Users\Rodrigo\Downloads\representation-for-ingredients\test.json\ingredients\train.txt')
    nouns_set = extract_nouns(r'Scraping\Datos\processed\primeros\video__KwZPgxQnmc.txt')
    with open(r'C:\Users\Rodrigo\Downloads\representation-for-ingredients\test.json\ingredients\train.txt','r+') as file:
        data = file.readlines()
        wnl = WordNetLemmatizer()
        data[:] = [wnl.lemmatize(line.strip()) for line in data]
        ingredients_set = set(data)
        nouns_set = set(nouns_set)
        result = ingredients_set.intersection(nouns_set)
        print(list(result))

def write_ingredients(ingredients:set , parent_folder: str, file_name: str)-> None:
    if not os.path.exists(os.path.join(OUTPUT_DIR, parent_folder)):
        os.mkdir(os.path.join(OUTPUT_DIR,parent_folder))

    with open( os.path.join(OUTPUT_DIR, parent_folder, file_name), 'w+', encoding='utf-8') as file:
        file.writelines('\n'.join(ingredients))

if __name__ == '__main__':
    ingredients_set = read_ingredients(INGREDIENTS_TXT_FILE)
    for root, dirs, files in os.walk(VIDEO_TXT_DIR, topdown=True):
        dirs[:] =  [d for d in dirs if d not in excluded]
        for file in files:
            if file.endswith('txt'):
                nouns_set = extract_nouns(os.path.join(root,file))
                result = ingredients_set.intersection(nouns_set)
                write_ingredients(result, os.path.basename(root), file)
                print(datetime.now().strftime('%d-%m-%Y %H:%M:%S'), file)
