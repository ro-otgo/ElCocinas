"""
Este script tiene como objetivo convertir los transcripciones json que se han 
descargado en ficheros de tipo texto.
"""
import os
import json
import csv

TRANSCRIPT_DIR = 'transcript'
PROCESSED_DIR = 'processed'
EXCLUDED_DIRS = ['processed',] + [TRANSCRIPT_DIR]
JSON_JOINED_NAME = 'contenido.json'

def convert_to_text(root_path: os.path = TRANSCRIPT_DIR):
    for dirpath, dirnames, filenames in os.walk(root_path):
        dirnames[:] = [d for d in dirnames if d not in EXCLUDED_DIRS]
        dir_name = os.path.join(root_path, PROCESSED_DIR, os.path.basename(dirpath))
        create_proccessed_folder(dir_name)
        for file_name in filenames:
            if file_name.endswith('.json'):
                with open(os.path.join(dirpath,file_name), 'r') as file:
                    file_content = json.load(file)
                    text_video = ' '.join(map(lambda x: x.get('text'), file_content))
                    text_video = text_video.replace('\n','. ')
                    file_name_output = os.path.splitext(file_name)[0] + '.txt'
                    with open(os.path.join(dir_name, file_name_output), 'w+', encoding='utf-8') as file_txt:
                        file_txt.writelines(text_video)

def join_json(root_path: os.path = TRANSCRIPT_DIR, file_output_name: os.path = JSON_JOINED_NAME):
    json_content = {}
    for dirpath, dirnames, filenames in os.walk(root_path):
        dirnames[:] = [d for d in dirnames if d not in EXCLUDED_DIRS]
        dir_name = os.path.join(root_path, PROCESSED_DIR, os.path.basename(dirpath))
        create_proccessed_folder(dir_name)
        for file_name in filenames:
            if file_name.endswith('.json'):
                with open(os.path.join(dirpath,file_name), 'r') as file:
                    file_content = json.load(file)
                    text_video = ' '.join(map(lambda x: x.get('text'), file_content))
                    text_video = text_video.replace('\n','. ')
                    video_id = file_name.split('video_')[1]
                    video_data = json_content.setdefault(video_id, {})
                    video_data['text'] = text_video
                    video_data['labels'] = []
                    # json_content[video_id] = text_video

    with open(os.path.join(TRANSCRIPT_DIR, PROCESSED_DIR, file_output_name), 'w+', encoding='utf-8') as file_txt:
        json.dump(json_content,file_txt, indent=2)

def create_csv(root_path: os.path = TRANSCRIPT_DIR, file_output_name: os.path = JSON_JOINED_NAME):
    dict_data = {}
    for dirpath, dirnames, filenames in os.walk(root_path):
        dirnames[:] = [d for d in dirnames if d not in EXCLUDED_DIRS]
        dir_name = os.path.join(root_path, PROCESSED_DIR, os.path.basename(dirpath))
        create_proccessed_folder(dir_name)
        for file_name in filenames:
            if file_name.endswith('.json'):
                with open(os.path.join(dirpath,file_name), 'r') as file:
                    file_content = json.load(file)
                    text_video = ' '.join(map(lambda x: x.get('text'), file_content))
                    text_video = text_video.replace('\n','. ')
                    video_id = file_name.split('video_')[1]
                    video_data = dict_data.setdefault(video_id, {})
                    video_data['text'] = text_video
                    video_data['labels'] = []
                    # json_content[video_id] = text_video
    csv_columns = ['name','text','labels']
    with open(os.path.join(TRANSCRIPT_DIR, PROCESSED_DIR, 'texto.csv'), 'w+', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=csv_columns, delimiter=';', escapechar='\\')
        writer.writeheader()
        for k,v in dict_data.items():
            data = {'name':k, 'text':v['text'], 'labels':v['labels']}
            writer.writerow(data)

def create_proccessed_folder(dir_name: str):
    if not os.path.exists(dir_name):
        os.mkdir(dir_name)

if __name__ == '__main__':
    create_proccessed_folder(os.path.join(TRANSCRIPT_DIR, PROCESSED_DIR))
    create_csv()
    join_json()
    convert_to_text(os.path.join('.',TRANSCRIPT_DIR))
