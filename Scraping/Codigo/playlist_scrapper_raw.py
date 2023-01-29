"""
Este script tiene como objetivo obtener las urls de los videos de una playlist.
Para ello se deberan modificar la url de la playlist a descargar.

El resultado de la operacion es un fichero tipo .txt en el que cada línea del 
fichero corresponde a una url del video de la playlist.
El nombre del fichero corresponde al nombre de la playlist.

Parametros a configurar:
- PLAYLIST_URL = Url de la playlist a descargar.

NOTA: 
Este script se desarrolla ya que la libreria pytube no puede obtener la 
informacion de los videos de una playlist.
Para poder ejecutar este scrip es necesario tener configurado el webdriver de 
selenium.
"""

__author__ = "ro-otgo"

from urllib import parse
import requests
from bs4 import BeautifulSoup
import os
from selenium.webdriver.chrome.service import Service
from selenium import webdriver
from selenium.webdriver.common.by import By
import random
import time

PLAYLIST_URL = 'https://www.youtube.com/playlist?list=PL2LHabI5sYyEyyuDesusF4FwGXjePVz37'
# PLAYLIST_URL = 'https://www.youtube.com/playlist?list=PLziprGSUFGYS4mxSpg3ZGxyVbTXEY9c_B'

GECKO_DRIVER = r"Scraping\Codigo\web_driver\geckodriver.exe"

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

def __scroll_through_whole_page(driver)-> None:
    # Metodo adaptado de: https://stackoverflow.com/a/27760083/8873596
    SCROLL_PAUSE_TIME = 0.5

    # Get scroll height
    # last_height = driver.execute_script("return document.body.scrollHeight")
    last_height = driver.execute_script("return document.documentElement.scrollHeight")

    while True:
        # Scroll down to bottom
        # driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        driver.execute_script("window.scrollTo(0, " + str(last_height) + ");")

        # Wait to load page
        time.sleep(random.uniform(0,3) + SCROLL_PAUSE_TIME)

        # Calculate new scroll height and compare with last scroll height
        # new_height = driver.execute_script("return document.body.scrollHeight")
        new_height = driver.execute_script("return document.documentElement.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height


def request_selenium(playlist_url: str, playlist_name: str, headless: bool = False)-> None:
    service = Service(executable_path=GECKO_DRIVER)
    options =  webdriver.FirefoxOptions()
    options.headless = headless
    driver = webdriver.Firefox(service=service, options= options)
    if driver.caps.get("moz:headless", False):
        # https://stackoverflow.com/a/74301253
        print("Firefox is headless")
    else:
        driver.maximize_window()
    driver.get(playlist_url)
    # driver.implicitly_wait(random.randint(0,3))
    if 'consent.youtube.com' in driver.current_url:
        try:
            driver.find_element(By.XPATH,'/html/body/c-wiz/div/div/div/div[2]/div[1]/div[3]/div[1]/form[1]/div/div/button/span').click()
            # driver.find_element(By.XPATH,'//button[@class="VfPpkd-LgbsSe VfPpkd-LgbsSe-OWXEXe-k8QpJ VfPpkd-LgbsSe-OWXEXe-dgl2Hf nCP5yc AjY5Oe DuMIQc LQeN7 IIdkle"]').click() 
        except Exception as e:
            print (e)
    
    __scroll_through_whole_page(driver)
    

    with open('cache_{name}.html'.format(name=playlist_name),'w+', encoding="utf-8") as f:
        f.write(driver.page_source)
    if driver:
        driver.close()


def parse_page(playlist_name: str)-> list:
    data = None
    with open('cache_{name}.html'.format(name=playlist_name),'r+',encoding="utf-8") as f:
        data = f.read()

    # soup =  BeautifulSoup(driver.page_source,'html.parser')
    soup =  BeautifulSoup(data,'html.parser')
    videos = soup.find_all(id = 'video-title', attrs={'class':'yt-simple-endpoint style-scope ytd-playlist-video-renderer'})
    playlist = []
    for link_video in videos:
        v = link_video['href']
        query_parsed = parse.urlparse(v)
        url_params = query_parsed.query
        data = parse.parse_qs(url_params)
        video_id = data.get('v')
        if video_id:
            video_id = "https://www.youtube.com/watch?v={video}".format(video=video_id[0])
            playlist.append(video_id)
    return playlist

def test_parsing()-> None:
    lista = ["/watch?v=iAo9Q0_-fDk&list=PLcApjfOBgcUquP-DYohxgsw3IjXStBAHC&index=23",
    "/watch?v=WYpF9QenmWA&list=PLcApjfOBgcUquP-DYohxgsw3IjXStBAHC&index=24",
    "/watch?v=K4c0ACPgY64&list=PLcApjfOBgcUquP-DYohxgsw3IjXStBAHC&index=25",
    "/watch?v=UA5IvaZ_Fxg&list=PLcApjfOBgcUquP-DYohxgsw3IjXStBAHC&index=26",
    "/watch?v=Q6D5rpuooI8&list=PLcApjfOBgcUquP-DYohxgsw3IjXStBAHC&index=27"]
    for l in lista:
        query_parsed = parse.urlparse(l)
        url_params = query_parsed.query
        data = parse.parse_qs(url_params)
        video_id = data.get('v')
        if video_id:
            print("https://www.youtube.com/watch?v={video}".format(video=video_id[0]))

def request_module()-> None:
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:108.0) Gecko/20100101 Firefox/108.0'}
    base_url = "https://www.youtube.com/playlist?list=PLcApjfOBgcUquP-DYohxgsw3IjXStBAHC"
    response = requests.get(base_url, headers=headers, cookies = {'CONSENT' : 'YES+'})
    if not os.path.exists('cache.html'):
        with open('cache.html', 'wb') as f:
            f.write(response.content)
    with open('cache.html', 'rb') as f:
        soup = BeautifulSoup(f.read(), 'html.parser')
        videos = soup.find_all(id = 'video-title', attrs={'class':'yt-simple-endpoint style-scope ytd-playlist-video-renderer'})
        for v in videos:
            query_parsed = parse.urlparse(v)
            url_params = query_parsed.query
            data = parse.parse_qs(url_params)
            video_id = data.get('v')
            if video_id:
                print("https://www.youtube.com/watch?v={video}".format(video=video_id[0]))

if __name__ == "__main__":
    # request_module()
    # test_parsing()
    output_name = retrive_playlist_name(PLAYLIST_URL)
    name = output_name.split("playlist_")[-1]
    cache_name = name.split(".")[0]

    request_selenium(playlist_url=PLAYLIST_URL, playlist_name=cache_name, headless=True)
    videos_url = parse_page(cache_name)
    with open(output_name,'w+') as file:
        file.writelines('\n'.join(videos_url))

