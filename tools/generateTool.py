import os
import threading
from tools.runModelEditor import runModelEditor
import tools


def generateTool(image_path):

    t = threading.Thread(
        target=generate(image_path),
        daemon=True,
    )
    t.start()
    # print('The model has been successfully generated!')
    # runModelEditor(image_path)


def create_generation_cmd(image_path):
    cmd = 'python src/pose.py --save-path output --img-path ' + \
          image_path + ' --use-natural --use-cos --use-angle-transf'
    file = open('generate.bat', 'w', encoding='utf-8')
    file.write(cmd)
    file.close()


def generate(image_path):
    create_generation_cmd(image_path)
    print('Create generate.bat')

    os.system('generate.bat')
    print('The model has been successfully generated!')
