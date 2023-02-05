"""
Este script tiene como objetivo ajustar las variables de entorno de cada equipo del 
proyecto de Rapidminer. Para ello se deberan modificar las siguientes variables
- STOP_WORDS_FILE = Ruta del diccionario de las stop words
- RAPIDMINER_FILE = Archivo donde esta almacenado el rapidminer
- POSTRES_DIRECTORY = Directorio donde estan los ficheros de los postres
- PRIMEROS_DIRECTORY = Directorio donde estan los ficheros de los primeros
- SEGUNDOS_DIRECTORY= Directorio donde estan los ficheros de los segundos
Tras la ejecucion del script se escribira el proceso en un archivo tipo xml con el 
siguiente nombre:
- SALIDA_FILE  = Nombre del archivo resultado
"""

__author__ = "ro-otgo"

import xml.etree.ElementTree  as ET
import os

RAPIDMINER_FILE = r'RapidMiner\ProyectoClasificador_varios.rmp'
STOP_WORDS_FILE = r'RapidMiner\StopWords\stopwords.txt'
POSTRES_DIRECTORY = r'Scraping\Datos\processed\postres'
PRIMEROS_DIRECTORY = r'Scraping\Datos\processed\primeros'
SEGUNDOS_DIRECTORY= r'Scraping\Datos\processed\segundos'
SALIDA_FILE = None

def proyecto_clasificador_varios(SALIDA_FILE: str = SALIDA_FILE)-> None:
    if SALIDA_FILE is None:
        SALIDA_FILE = RAPIDMINER_FILE.replace('.rmp','_rodrigo.rmp')

    tree = ET.parse(RAPIDMINER_FILE)
    root = tree.getroot()
    primeros_element = root.find(".//*[@key='Primeros']")
    primeros = primeros_element.attrib
    primeros['value'] = os.path.abspath(os.path.join('.',PRIMEROS_DIRECTORY))
    
    segundos_element = root.find(".//*[@key='Segundos']")
    segundos = segundos_element.attrib
    segundos['value'] = os.path.abspath(os.path.join('.',SEGUNDOS_DIRECTORY))
    
    postres_element = root.find(".//*[@key='Postres']")
    postres = postres_element.attrib
    postres['value'] = os.path.abspath(os.path.join('.',POSTRES_DIRECTORY))

    filter_stopwords_dictionary = root.find(".//*[@class='text:filter_stopwords_dictionary']/parameter[@key='file']")
    data_filter_stopwords_dictionary = filter_stopwords_dictionary.attrib
    data_filter_stopwords_dictionary['value'] = os.path.abspath(os.path.join('.',STOP_WORDS_FILE))
    tree.write(SALIDA_FILE, encoding='UTF-8', xml_declaration=True)

if __name__ == "__main__":
    proyecto_clasificador_varios()
