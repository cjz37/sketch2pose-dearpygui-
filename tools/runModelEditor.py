import os
import threading


def runModelEditor(image_path):
    create_open_cmd(image_path)
    print('create open.bat')
    run()
    print('run model editor')


def create_open_cmd(image_path):
    cmd = 'python ModelEditor.py --image-path ' + image_path
    file = open('runModelEditor.bat', 'w', encoding='utf-8')
    file.write(cmd)
    file.close()


def run():
    os.system('runModelEditor.bat')
