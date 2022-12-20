import os
import json

transcript_dir = 'transcript'
processed_dir = 'processed'

def convert_to_text(root_path:os.path):
    for dirpath, dirnames, filenames in os.walk(root_path):
        dirnames[:] = [d for d in dirnames if d not in [processed_dir]]
        dir_name = os.path.join(root_path, processed_dir, os.path.basename(dirpath))
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

def create_proccessed_folder(dir_name):
    if not os.path.exists(dir_name):
        os.mkdir(dir_name)

if __name__ == '__main__':
    create_proccessed_folder(os.path.join(transcript_dir, processed_dir))
    convert_to_text(os.path.join('.',transcript_dir))
