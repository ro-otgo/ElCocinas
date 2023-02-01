"""
Este script se encarga de adaptar la lista original de los ingredientes a un 
formato más sencillo de trabajar con el. 

La lista original de ingredientes se ha obtenido de: https://www.bedca.net/bdpub/index.php
Variables:
RUTA_INGREDIENTES_ORIGINAL = 'ingredientes_espanol.csv'
FICHERO_INGREDIENTES_RAW = 'ingredientes-raw-es.txt'
FICHERO_INGREIDNTES_PROCESADO = 'ingredientes-processed-es.txt'

"""
import csv
import unicodedata

__author__ = 'ro-otgo'

RUTA_INGREDIENTES_ORIGINAL = r'ETL\Codigo\ingredients\dataset_ingredients\ingredientes_espanol\ingredientes_espanol.csv'
FICHERO_INGREDIENTES_RAW = r'ETL\Codigo\ingredients\dataset_ingredients\ingredientes_espanol\ingredientes-raw-es.txt'
FICHERO_INGREIDNTES_PROCESADO = r'ETL\Codigo\ingredients\dataset_ingredients\ingredientes_espanol\ingredientes-processed-es.txt'

def read_file(ingredients_path:str)-> dict:
    with open(ingredients_path,'r', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile,delimiter='\t',fieldnames=['id','es','en'])
        data = {}
        for row in reader:
            ingredient = data.setdefault(row['id'],{})
            ingredient['es'] = row['es']
            ingredient['en'] = row['en']
        return data

def get_data_es(data:dict)->list:
    es_data = []
    for k in data.keys():
        ingredient = data.get(k)
        es_data.append(ingredient['es'])
    return es_data

def write_ingredientes_es_raw(data:list)->None:
    with open(FICHERO_INGREDIENTES_RAW,'w+') as file:
        file.writelines('\n'.join(data))

def limpiar_text(text:str)->str:
    # https://stackoverflow.com/a/518232/8873596
    return ''.join(c for c in unicodedata.normalize('NFD', text)
                  if unicodedata.category(c) != 'Mn')
import string

def eliminar_punctuation(text:str)->str:
    not_valid = string.punctuation + 'º°' + string.digits
    text = ''.join(map(lambda t: t.replace(t,'') if t in not_valid else t ,text))
    return text

def write_ingredientes_es_processed(data:list)->None:
    data[:] = list(map(lambda ingredient: limpiar_text(ingredient), data))
    data[:] = list(map(lambda ingredient: eliminar_punctuation(ingredient).lower(), data))
    with open(FICHERO_INGREIDNTES_PROCESADO,'w+') as file:
        file.writelines('\n'.join(data))

if __name__ == '__main__':
    data = read_file(RUTA_INGREDIENTES_ORIGINAL)
    ingredientes_esp = get_data_es(data)
    write_ingredientes_es_raw(ingredientes_esp)
    write_ingredientes_es_processed(ingredientes_esp)
