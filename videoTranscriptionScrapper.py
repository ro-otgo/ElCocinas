from youtube_transcript_api import YouTubeTranscriptApi
import json

def downloadVideoScript(videoId:str):
    transcript_list = YouTubeTranscriptApi.list_transcripts(videoId)
    transcript = transcript_list.find_transcript(['en'])
    data_transcript = transcript.fetch()
    with open('video_{}.json'.format(videoId), 'w', encoding='utf-8') as file:
        file.write(json.dumps(data_transcript,indent=2))


if __name__ == "__main__":
    downloadVideoScript('Ge7c7otG2mk')