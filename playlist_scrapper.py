
from pytube import YouTube
from pytube import Playlist


if __name__ == "__main__":
    playlist_url = 'https://www.youtube.com/playlist?list=PLnujfCpADfgcntTD26TzIz9gbol97JfUa'
    p = Playlist(playlist_url)
    videos_url = p.video_urls
    with open('playlist?list=PLnujfCpADfgcntTD26TzIz9gbol97JfUa.txt','w') as file:
        file.writelines('\n'.join(videos_url))
