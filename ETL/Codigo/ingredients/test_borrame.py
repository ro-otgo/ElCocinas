data_lemmatize = ['wine', 'juice', 'broiler', 'rooster', 'corn', 'beef', 'pepper', 'pumpkin', 'hand', 'curry', 'cream', 'meat', 'chocolate', 'salt', 'spinach', 'bacon', 'cheese', 'sugar']
data_no =  ['wine', 'corn', 'sugar', 'spinach', 'juice', 'bacon', 'chips', 'pepper', 'cheese', 'beef', 'broiler', 'curry', 'pumpkin', 'cream', 'crackers', 'salt', 'meat']
full = ['salsa', 'artichokes', 'pumpkin', 'olives', 'bacon', 'pepper', 'crackers', 'juice', 'salt', 'Velveeta', 'beef', 'meat', 'chips', 'cream', 'onions', 'corn', 'sugar', 'cheese', 'wine', 'spinach', 'broiler', 'curry']

otro = ['wine', 'rooster', 'chocolate', 'orange', 'pepper', 'beef', 'sugar', 'spinach', 'juice', 'cheese', 'curry', 'corn', 'pumpkin', 'hand', 'broiler', 'popcorn', 'bacon', 'meat', 'cream', 'salt', 'steak']

data_ok = ['wine', 'crisp', 'meat', 'pepper', 'sugar', 'corn', 'steak', 'rooster', 'orange', 'artichoke', 'onion', 'beef', 'chip', 'popcorn', 'chocolate', 'hand', 'curry', 'broiler', 'spinach', 'salt', 'pumpkin', 'cheese', 'cream', 'juice', 'sausage', 'bacon', 'sandwich', 'spice']
print(sorted(data_lemmatize))
print(sorted(data_no))
print(sorted(full))
print(sorted(otro))

import logging
from logging import Logger
logger = logging.getLogger()
print(type(logger),Logger.__name__)

spacy_data = ['cheese', 'rooster', 'curry', 'sugar', 'artichoke', 'meat', 'steak', 'seasoning', 'chip', 'spice', 'salsa', 'orange', 'cream', 'onion', 'beef', 'broiler', 'sandwich', 'tea', 'spinach', 'hand', 'pumpkin', 'chocolate', 'wine', 'sausage', 'bacon', 'crab', 'pepper', 'juice', 'popcorn', 'kale', 'corn', 'salt', 'olive']
ntlk_data = ['sandwich', 'wine', 'rooster', 'chocolate', 'salt', 'spinach', 'pepper', 'beef', 'spice', 'popcorn', 'chip', 'sugar', 'onion', 'broiler', 'corn', 'crisp', 'curry', 'sausage', 'artichoke', 'cheese', 'cream', 'meat', 'pumpkin', 'orange', 'juice', 'hand', 'bacon', 'steak']
ntlk_data2 = ['cheese', 'rooster', 'curry', 'sugar', 'artichoke', 'meat', 'steak', 'chip', 'spice', 'orange', 'cream', 'crisp', 'onion', 'beef', 'broiler', 'sandwich', 'spinach', 'hand', 'pumpkin', 'chocolate', 'wine', 'sausage', 'bacon', 'pepper', 'juice', 'popcorn', 'corn', 'salt']
print('SPACY_DATA:')
print(sorted(spacy_data))
print('NLTK_DATA:')
print(sorted(ntlk_data))
print('NLTK_DATA2:')
print(sorted(ntlk_data2))
print("differences")
print(set(ntlk_data).difference(set(spacy_data)))
print(set(spacy_data).difference(set(ntlk_data)))

