"""
Este script se encarga de adaptar la lista original de los ingredientes a un 
formato más sencillo de trabajar con el. 

La lista original de ingredientes se ha obtenido de:
https://www.kaggle.com/datasets/kaggle/recipe-ingredients-dataset?select=train.json
Variables:
LISTA_ORIGINAL = r'ETL\Codigo\ingredients\dataset_ingredients\representation-for-ingredients\train.json'
FICHERO_SALIDA = r'ETL\Codigo\ingredients\dataset_ingredients\representation-for-ingredients\train.txt'
"""
import json

__author__ = 'ro-otgo'

LISTA_ORIGINAL = r'ETL\Codigo\ingredients\dataset_ingredients\representation-for-ingredients\train.json'
FICHERO_SALIDA = r'ETL\Codigo\ingredients\dataset_ingredients\representation-for-ingredients\train.txt'

def extract_ingredients(file_path, output_file):
    ingredients_set = set()
    with open(file_path, "r+", encoding="utf-8") as f:
        data = json.load(f)
        print(file_path + " :", len(data))
        for item in data:
            ingredients_set.update(item['ingredients'])
    ingredients_list = list(ingredients_set)
    with open(output_file, 'w+', encoding='utf-8') as file:
        file.writelines('\n'.join(ingredients_list))

if __name__ == "__main__":
    extract_ingredients(LISTA_ORIGINAL, FICHERO_SALIDA)