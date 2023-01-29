"""
Script auxiliar para procesar la lista original de ingredientes.
La lista origintal de ingredientes se puede localizar en el siguiente repositorio:
https://github.com/schollz/food-identicon/blob/master/ingredients.txt
Ademas se ha almacenado en el proyecto para tenerla de referencia por si fuera 
necesario referirse a ella.
"""
from nltk.corpus import words
from nltk.tokenize import wordpunct_tokenize

def filter_list_one(file_path:str )-> list:
    list_filtered = set()
    with open(file_path,'r',encoding='utf-8') as file:
        lines = file.readlines()
        lines = [l.strip() for l in lines]
        lines_len = len(lines)
        for line_number, line in enumerate(lines):
            print(line_number/float(lines_len) * 100.0 )
            for word in wordpunct_tokenize(line):
                if word in words.words():
                    list_filtered.add(word)
    return list_filtered
def filter_list_two(file_path:str )-> list:
    list_filtered = set()
    with open(file_path,'r',encoding='utf-8') as file:
        lines = file.readlines()
        lines = [l.strip() for l in lines]
        lines_len = len(lines)
        for line_number, word in enumerate(lines):
            print(line_number/float(lines_len) * 100.0 )
            if word in words.words():
                list_filtered.add(word)
    return list_filtered

def write_list(ingredient_list:list, output_name: str)-> None:
    with open(output_name,'w+') as file:
        file.writelines('\n'.join(ingredient_list))
if __name__ == '__main__':
    ingredient_list = filter_list_one(r'ETL\Codigo\ingredients\output\ingredients.txt')
    write_list(ingredient_list, output_name=r'ETL\Codigo\ingredients\output\ingredients_ok.txt')
    ingredient_list = filter_list_two(r'ETL\Codigo\ingredients\output\ingredients.txt')
    write_list(ingredient_list, output_name=r'ETL\Codigo\ingredients\output\ingredients_ok2.txt')
