import os
import threading
from tools.runModelEditor import runModelEditor


def generateTool(image_path):
    create_generation_cmd(image_path)
    print('Create generate.bat')
    generate()
    print('The model has been successfully generated!')
    runModelEditor(image_path)


def create_generation_cmd(image_path):
    cmd = 'python src/pose.py --save-path output --img-path ' + \
          image_path + ' --use-cos --use-angle-transf --use-natural'
    file = open('generate.bat', 'w', encoding='utf-8')
    file.write(cmd)
    file.close()


def generate():
    os.system('generate.bat')
