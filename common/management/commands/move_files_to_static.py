import os
import glob
import shutil

def move_files():
    files = glob.glob('experiments/current/*/files/*.css') + \
            glob.glob('experiments/current/*/files/*.js') + \
            glob.glob('common/templates/*.js') + \
            glob.glob('common/templates/*.css') + \
            glob.glob('experiments/current/*/stimuli/*') 


    for f in files:
        os.makedirs(os.path.dirname(os.path.join('static',f)), exist_ok=True) # if the path doesn't exist yet, make it first
        shutil.copyfile(f, os.path.join('static', f))


if __name__=='__main__':
    move_files()
