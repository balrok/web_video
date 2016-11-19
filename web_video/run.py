#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# check dir for files older 60s so we are sure to have complete transfered files
# then create a tmp dir for them
# put a screenshot
# use bento4 to create different qualities
#     hls
#     dash
#     webm
# when finished remove file and move tmp directory

try:
    from os import scandir
except ImportError:
    from scandir import scandir
import sys
import os
import json
from time import time
from tempfile import TemporaryDirectory
from subprocess import CalledProcessError, run, PIPE
import urllib.request

from lib.singleton import SingleInstance


def main(root_dir:str, callback_url:str):
    return_code = 0
    for e in scandir(root_dir):
        if e.is_dir():
            print(e.name)
            dir = os.path.join(root_dir, e.name)
            changed = False
            for entry in scandir(dir):
                if entry.is_dir():
                    continue
                name = entry.name
                if entry.stat().st_mtime + 60 > time():
                    print("Modified too recently: {}".format(time() - entry.stat().st_mtime))
                    continue
                if os.path.splitext(name)[1][1:].lower() in ("mp4", "mts", "webm", "mpg", "mpeg"):
                    print("Found a file {}".format(name))
                    if not process_vid(name, dir):
                        sys.stderr.write("ERROR: {} could not be processed\n".format(name))
                        return_code = -1
                    else:
                        changed = True
                if os.path.splitext(name)[1][1:].lower() in ("jpg", "png"):
                    print("Found a file {}".format(name))
                    if not process_img(name, dir):
                        sys.stderr.write("ERROR: {} could not be processed\n".format(name))
                        return_code = -1
                    else:
                        changed = True
            if changed:
                urllib.request.urlopen(callback_url).read()
    sys.exit(return_code)

def process_img(name:str, path:str):
    return False
    name_no_ext, ext = os.path.splitext(name)
    file = os.path.join(path, name)
    target_folder = os.path.join(path, name_no_ext)
    if os.path.exists(target_folder):
        print("Cannot process {} as the target folder {} already exists".format(name, target_folder))
        return False
    with TemporaryDirectory() as temp_dir:
        print("using tempdir {}".format(temp_dir))
        # convert dragon.gif    -resize 4096@>  pixel_dragon.gif
        for s in (2048, 1024, 512, 256):
            print("convert {} -resize {size}x{size}\\> {tmp}/{size}.jpg".format(file, size=s, tmp=temp_dir))
            run("convert {} -resize {size}x{size}\\> {tmp}/{size}.jpg".format(file, size=s, tmp=temp_dir), shell=True, stdout=sys.stdout)
        #run("mkdir {}".format(target_folder), shell=True, stdout=sys.stdout)
        run("mv {}/* {}".format(temp_dir, target_folder), shell=True, stdout=sys.stdout)
        run("mv {} {}/orig.{}".format(file, target_folder, ext), shell=True, stdout=sys.stdout)


def process_vid(name:str, path:str):
    name_no_ext, ext = os.path.splitext(name)
    file = os.path.join(path, name)
    target_folder = os.path.join(path, name_no_ext)
    if os.path.exists(target_folder):
        print("Cannot process {} as the target folder {} already exists".format(name, target_folder))
        return False
    with TemporaryDirectory() as temp_dir:
        print("using tempdir {}".format(temp_dir))
        try:
            run("python `which mp4-dash-encode.py` -v -b 3 -o {}/v {}".format(temp_dir, file), shell=True, stdout=sys.stdout)
        except CalledProcessError:
            return False
        run("mp4dash -o {t}/dash {t}/v/*".format(t=temp_dir), shell=True, stdout=sys.stdout)
        run("mp4hls -o {t}/hls {t}/v/*".format(t=temp_dir), shell=True, stdout=sys.stdout)

        p = run("ffprobe -v quiet -print_format json -show_streams {}".format(file), shell=True, universal_newlines=True, stdout=PIPE)
        d = json.loads(p.stdout, strict=False)
        duration = int(float(d["streams"][0]["duration"]))

        run("ffmpeg -i {} -vf fps={}/{} {}/img_%d.jpg".format(file, 5, duration, temp_dir), shell=True, stdout=sys.stdout)
        run("ffmpeg -i {} -c:v libvpx -b:v 1M -c:a libvorbis -vf \"scale='min(600,iw)':-1\" {}/video.webm".format(file, temp_dir), shell=True, stdout=sys.stdout)
        run("mkdir {}".format(target_folder), shell=True, stdout=sys.stdout)
        run("mv {}/dash/* {}".format(temp_dir, target_folder), shell=True, stdout=sys.stdout)
        run("mv {}/hls/* {}".format(temp_dir, target_folder), shell=True, stdout=sys.stdout)
        run("mv {}/img_* {}".format(temp_dir, target_folder), shell=True, stdout=sys.stdout)
        run("mv {}/video_* {}".format(temp_dir, target_folder), shell=True, stdout=sys.stdout)
        run("mv {} {}/orig.{}".format(file, target_folder, ext), shell=True, stdout=sys.stdout)
        print("moved all to {}".format(target_folder))
    return True
	
def run():
    SingleInstance("videotransformer")
    # first argument is folder which we will check
    main(sys.argv[1], sys.argv[2])


if __name__ == "__main__":
    run()
