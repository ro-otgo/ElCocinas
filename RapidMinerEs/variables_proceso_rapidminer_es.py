"""
Este script tiene como objetivo ajustar las variables de entorno de cada equipo del 
proyecto de Rapidminer. Para ello se deberan modificar las siguientes variables
- STOP_WORDS_FILE = Ruta del diccionario de las stop words
- POSTRES_DIRECTORY = Directorio donde estan los ficheros de los postres
- PRIMEROS_DIRECTORY = Directorio donde estan los ficheros de los primeros
- SEGUNDOS_DIRECTORY= Directorio donde estan los ficheros de los segundos

Tras la ejecucion del script se escribira el proceso en un archivo tipo xml con el 
siguiente nombre:
- SALIDA_FILE  = Nombre del archivo resultado + .rmp
"""

__author__ = "ro-otgo"

import xml.etree.ElementTree  as ET
import os

STOP_WORDS_FILE = r"RapidMinerEs\StopWordEs\StopWordsEs.txt"

POSTRES_DIRECTORY = r'RapidMinerEs\Datos\PostresEsp\transcript'
PRIMEROS_DIRECTORY = r'RapidMinerEs\Datos\PrimerosEsp\transcript'
SEGUNDOS_DIRECTORY= r'RapidMinerEs\Datos\SegundosEsp\transcript'

def leer_modelo(path_model:str):
    tree = ET.parse(path_model)
    return tree

def adaptar_modelos_rapidminer_es(rapidminer_model_path:str)-> None:
    SALIDA_FILE = rapidminer_model_path.replace('.rmp','_rodrigo.rmp')
    tree = leer_modelo(rapidminer_model_path)
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
    rapidminer_files = [
        r'RapidMinerEs\Modelos\ModeloDeepLearnEs.rmp',
        r'RapidMinerEs\Modelos\ModeloKnnEs.rmp',
        r'RapidMinerEs\Modelos\ModeloRanForEs.rmp',
        r'RapidMinerEs\Modelos\ModeloSvmEs.rmp',
    ]
    for rapidminer_file in rapidminer_files:
        adaptar_modelos_rapidminer_es(rapidminer_model_path=rapidminer_file)
