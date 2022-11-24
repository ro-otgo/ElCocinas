from youtube_transcript_api import YouTubeTranscriptApi
import json
import os

def create_transcript_folder(transcript_folder:str):
    if not os.path.exists(transcript_folder):
        os.mkdir(transcript_folder)

def downloadVideoScript(videoId:str, transcript_folder='transcript'):
    transcript_list = YouTubeTranscriptApi.list_transcripts(videoId)
    transcript = transcript_list.find_transcript(['en'])
    data_transcript = transcript.fetch()
    with open(os.path.join(transcript_folder,'video_{}.json'.format(videoId)), 'w', encoding='utf-8') as file:
        file.write(json.dumps(data_transcript,indent=2))


if __name__ == "__main__":
    create_transcript_folder('transcript')
    downloadVideoScript('Ge7c7otG2mk')
