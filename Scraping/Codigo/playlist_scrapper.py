"""
Este script tiene como objetivo obtener las urls de los videos de una playlist.
Para ello se deberan modificar la url de la playlist a descargar.

El resultado de la operacion es un fichero tipo .txt en el que cada línea del 
fichero corresponde a una url del video de la playlist.
El nombre del fichero corresponde al nombre de la playlist.

Parametros a configurar:
- PLAYLIST_URL = Url de la playlist a descargar.
"""

__author__ = "ro-otgo"

from pytube import Playlist
from urllib import parse

# PLAYLIST_URL = 'https://www.youtube.com/watch?v=VdWM48aTiXA&list=PL2LHabI5sYyEyyuDesusF4FwGXjePVz37'
PLAYLIST_URL = 'https://www.youtube.com/watch?v=a9lZ765L_P0&list=PLziprGSUFGYS4mxSpg3ZGxyVbTXEY9c_B'

def retrive_playlist_name(playlist_url: str)-> str:
    playlist_parsed = parse.urlparse(playlist_url)
    url_params = playlist_parsed.query
    data = parse.parse_qs(url_params)
    list_name = data.get('list')
    if list_name:
        playlist_name = list_name[0]
    else:
        playlist_name = 'unknown'
    return 'playlist_{name}.txt'.format(name=playlist_name)


if __name__ == "__main__":
    output_name = retrive_playlist_name(PLAYLIST_URL)
    p = Playlist(PLAYLIST_URL)
    videos_url = p.video_urls
    with open(output_name,'w+') as file:
        file.writelines('\n'.join(videos_url))
