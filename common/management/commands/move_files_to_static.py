import os
import glob
import shutil

def move_files():
    files = glob.glob('experiments/current/*/files/*.css') + \
            glob.glob('experiments/current/*/files/*.js')
    for f in files:
        shutil.copyfile(f, os.path.join('static', f))


if __name__=='__main__':
    move_files()
