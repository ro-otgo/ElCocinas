"""
Este script tiene como objetivo descargar las transcripciones de los videos que 
se indican.
Para ello se deberan incluir en un fichero de tipo texto en el que cada linea
del mismo es un video del cual se desea descargar la transcripcion.

El resultado de la operacion es un fichero tipo .json con el siguiente formato:
    - Para el video 'https://www.youtube.com/watch?v=ID_VIDEO' se generara el 
    json con el siguiente nombre: 'video_ID_VIDEO.json'
Este json contiene un array de objetos con el siguiente contenido:
    - 'text', 'start', 'duration'

Para poder supervisar el resultado de la operacion se generar un log con la 
ejecucion del programa. 
La informacion que se mostrara en el log se puede configurar mediante la 
variable: 'LOG_LEVEL'

Parametros a configurar;
- LOG_LEVEL = Nivel de logging que deseamos obtener en el proceso.
- SOURCE_VIDEOS = Ubicacion del archivo de texto donde estaran almacenados los 
    videos que se desean obtener la transcripcion.
- TRANSCRIPT_FOLDER = Carpeta donde se almacena la transcripcion de los videos.
"""
from youtube_transcript_api import YouTubeTranscriptApi
from urllib import parse
import logging
import json
import os

LOG_LEVEL = logging.INFO
SOURCE_VIDEOS = 'source_videos.txt'
TRANSCRIPT_FOLDER = 'transcript'

def create_transcript_folder(transcript_folder: str) -> None:
    if not os.path.exists(transcript_folder):
        os.mkdir(transcript_folder)
        logger.info('Se ha creado la carpeta %s', transcript_folder)

def download_video_transcript(video_id: str, transcript_folder: str = TRANSCRIPT_FOLDER) -> None:
    transcript_list = YouTubeTranscriptApi.list_transcripts(video_id)
    transcript = transcript_list.find_transcript(['en'])
    data_transcript = transcript.fetch()
    logger.debug('Se va a descargar la transcripcion del video : %s', video_id)
    with open(os.path.join(transcript_folder,'video_{}.json'.format(video_id)), 'w', encoding='utf-8') as file:
        file.write(json.dumps(data_transcript,indent=2))
    logger.debug('Se ha descargado el video : %s', video_id)

def load_youtube_files(file_path: str) -> list:
    videos_id_list = []
    with open(file_path,'r') as file:
        for l in file.readlines():
            try:
                logger.debug('Se va a obtener el id del video: %s',l.strip())
                url_parsed = parse.urlparse(l)
                query_data = url_parsed.query
                query = parse.parse_qs(query_data)
                videos_id = query.get('v', None)
                if not videos_id:
                    logger.error('El video \'%s\' no es tiene el formato esperado %s',l, query_data)
                    continue
                video_id = videos_id[0].strip()
                videos_id_list.append(video_id)
            except Exception as e:
                logger.error('Se ha producido una excepcion: %s', e)
    return videos_id_list

def crear_logger(level: int = LOG_LEVEL):
    print('crear logger')
    logger = logging.getLogger(__name__)

    formatter = logging.Formatter('%(asctime)s %(levelname)s %(lineno)d:%(filename)s - %(message)s')
    file_handler = logging.FileHandler(filename='transcripciones.log', mode='w+', encoding='utf-8')
    file_handler.setFormatter(formatter)

    logger.setLevel(level)
    # logging.basicConfig(format='%(asctime)s %(levelname)s %(lineno)d:%(filename)s - %(message)s', filename='transcripciones.log', encoding='utf-8', level = LOG_LEVEL)
    logging.getLogger('youtube_transcript_api').setLevel(logging.ERROR)
    logging.getLogger('request').setLevel(logging.ERROR)
    logging.getLogger('urllib').setLevel(logging.ERROR)
    logging.getLogger('urllib3').setLevel(logging.ERROR)

    logger.addHandler(file_handler)
    return logger

# logger = crear_logger()

logger = crear_logger(LOG_LEVEL)

if __name__ == "__main__":
    print('inicio')
    logger.info('inicio')
    create_transcript_folder(TRANSCRIPT_FOLDER)
    lista_videos = load_youtube_files(SOURCE_VIDEOS)
    logger.info('Se han obtenido %d videos', len(lista_videos))
    logger.info('Se van a descargar las transcripciones')
    for v in lista_videos:
        try:
            download_video_transcript(v)
        except Exception as e:
            logger.error('Se ha producido una excepcion procesando el video: %s', v)
    logger.info('Ha finalizado el programa')

