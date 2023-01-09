"""
Este script tiene como objetivo ajustar las variables de entorno de cada equipo del 
proyecto de Rapidminer. Para ello se deberan modificar las siguientes variables
- DATA_CAKE_DIR = Ruta de la carpeta de las tartas
- DESSERT_CAKE_DIR = Ruta de la carpeta de los postres
- STOP_WORDS_FILE = Ruta del diccionario de las stop words
- RAPIDMINER_FILE = Archivo donde esta almacenado el rapidminer
Tras la ejecucion del script se escribira el proceso en un archivo tipo xml con el 
siguiente nombre:
- SALIDA_FILE  = Nombre del archivo resultado
"""
import xml.etree.ElementTree  as ET


DATA_CAKE_DIR = r"C:/Users/jovig/Desktop/ProyectoCompu/arbol de decision/cake/transcript"
DESSERT_CAKE_DIR = r"C:/Users/jovig/Desktop/ProyectoCompu/arbol de decision/Postres/transcript"
STOP_WORDS_FILE = r"C:/Users/jovig/Desktop/ProyectoCompu/arbol de decision/StopWords/stopwords.txt"


RAPIDMINER_FILE = r'RapidMiner\ProyectoClasificador.rmp' 
SALIDA_FILE = r'output.rmp' 

if __name__ == "__main__":
    tree = ET.parse(RAPIDMINER_FILE)
    root = tree.getroot()
    procces_document = root.find(".//*[@class='text:process_document_from_file']")
    cake_directory = root.find(".//*[@key='Cake']")
    dessert_directory = root.find(".//*[@key='Dessert']")
    filter_stopwords_dictionary = root.find(".//*[@class='text:filter_stopwords_dictionary']/parameter[@key='file']")
    data_cake = cake_directory.attrib
    data_dessert_directory = dessert_directory.attrib
    data_filter_stopwords_dictionary = filter_stopwords_dictionary.attrib
    data_cake['value'] = DATA_CAKE_DIR
    data_dessert_directory['value'] = DESSERT_CAKE_DIR
    data_filter_stopwords_dictionary['value'] = STOP_WORDS_FILE

    tree.write(SALIDA_FILE, encoding='UTF-8', xml_declaration=True)
