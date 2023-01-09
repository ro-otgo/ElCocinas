
from pytube import YouTube
from pytube import Playlist


if __name__ == "__main__":
    playlist_url = 'https://www.youtube.com/watch?v=VdWM48aTiXA&list=PL2LHabI5sYyEyyuDesusF4FwGXjePVz37'
    p = Playlist(playlist_url)
    videos_url = p.video_urls
    with open('playlist_PL2LHabI5sYyEyyuDesusF4FwGXjePVz37.txt','w') as file:
        file.writelines('\n'.join(videos_url))
