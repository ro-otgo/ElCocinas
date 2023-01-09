from youtube_transcript_api import YouTubeTranscriptApi
import json
import os
import re

def create_transcript_folder(transcript_folder:str) -> None:
    if not os.path.exists(transcript_folder):
        os.mkdir(transcript_folder)

def downloadVideoScript(videoId:str, transcript_folder='primeros') -> None:
    transcript_list = YouTubeTranscriptApi.list_transcripts(videoId)
    transcript = transcript_list.find_transcript(['en'])
    data_transcript = transcript.fetch()
    with open(os.path.join(transcript_folder,'video_{}.json'.format(videoId)), 'w', encoding='utf-8') as file:
        file.write(json.dumps(data_transcript,indent=2))

def load_youtube_files(file_path:str) -> list:
    videos_id_list = []
    with open(file_path,'r') as file:
        for l in file.readlines():
            video_id = re.findall('.+youtube.+watch\?v=(\w+)',l)
            videos_id_list.extend(video_id)
    return videos_id_list

if __name__ == "__main__":
    create_transcript_folder('primeros')
    lista_videos = load_youtube_files('primeros.txt')
    for v in lista_videos:
        downloadVideoScript(v)
