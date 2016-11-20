from time import time
import os
from subprocess import CalledProcessError, run, PIPE, DEVNULL
import json
from shlex import quote
import unicodedata
import re
import sys
from tempfile import TemporaryDirectory
from zenlog import log

filetypes = []


process_stdout = sys.stdout # open(os.devnull, 'w')
process_stdout = DEVNULL
sub_run = run
def run(*args, **kwargs):
    if "shell" not in kwargs:
        kwargs["shell"] = True
    if "stdout" not in kwargs:
        kwargs["stdout"] = process_stdout
    if "stderr" not in kwargs:
        kwargs["stderr"] = process_stdout
    log.info("CMD: %s"% args[0])
    start = time()
    try:
        ret = sub_run(*args, **kwargs)
        if time()-start > 1:
            log.info("Took %d seconds" % int(time()-start))
        if ret.returncode != 0:
            return False
        return ret
    except (OSError, CalledProcessError) as e:
        log.error('While running a command an exception occured: %s', e)
        log.error(args)
        log.error(kwargs)
        return False

class BasicFile(object):
    ERROR = 0
    UPDATED = 1
    NO_CHANGE = 2

    ### Static methods
    def cmd_exists(program):
        v = run("which {}".format(program), stdout=PIPE)
        if v.stdout == b"":
            log.error("Program {} does not exist".format(program))
            return False
        return True

    def test_requirements():
        ret = True
        for f in filetypes:
            ret &= f.test_requirements()
        return ret

    def get_instance(entry):
        for f in filetypes:
            fh = f(entry)
            if fh.istype():
                return fh
        return None

    ### Instance methods
    def __init__(self, entry):
        self.entry = entry
        self.name = entry.name
        self.path = os.path.dirname(entry.path)
        self.is_processed_folder = False

    def getRunOpts(self):
        name_no_ext, ext = os.path.splitext(os.path.basename(self.getOrigFile()))
        return {
            'o': quote(self.getOrigFile()),
            'oe': ext.lower(),
            'tf': quote(self.getTargetFolder()),
            'path': self.path,
            'name': self.name,
            'name_no_ext': name_no_ext,
        }

    def getTargetFolder(self):
        def slugify(value):
            """
            Normalizes string, converts to lowercase, removes non-alpha characters,
            and converts spaces to hyphens.
            """
            value = unicodedata.normalize('NFKD', value).encode('ascii', 'ignore').decode("utf-8")
            value = re.sub('[^\w\s-]', '', value).strip().lower()
            return re.sub('[-\s]+', '_', value)
        file = os.path.join(self.path, self.name)
        name_no_ext, ext = os.path.splitext(os.path.basename(self.getOrigFile()))
        if os.path.isdir(file):
            return file
        else:
            return os.path.join(self.path, slugify(name_no_ext))

    def getOrigFile(self):
        if os.path.isdir(os.path.join(self.path, self.name)):
            for e in self.exts:
                path = os.path.join(self.path, self.name, "orig."+e)
                if os.path.exists(path):
                    return path
            return False
        else:
            return os.path.join(self.path, self.name)

    def istype(self):
        if self.entry.stat().st_mtime + 60 > time():
            log.debug("Modified too recently: %d", time() - self.entry.stat().st_mtime)
            return False
        return True

    def update(self, items):
        if not os.path.isdir(self.getTargetFolder()):
            return {"update":self.NO_CHANGE}
        ret = {}
        for i in items:
            try:
                ret[i[0]] = i[1]()
            except Exception:
                ret[i[0]] = self.ERROR
        return ret

    def process(self):
        if self.is_processed_folder:
            return self.update()
        if os.path.exists(self.getTargetFolder()):
            log.error("Cannot process {} as the target folder {} already exists".format(self.name, self.getTargetFolder()))
            return {"orig":self.ERROR}
        log.debug("mkdir {tf}".format(**self.getRunOpts()))
        run("mkdir {tf}".format(**self.getRunOpts()))
        run("mv {o} {tf}/orig{oe}".format(**self.getRunOpts()))
        self.name = os.path.basename(self.getTargetFolder())
        return self.update()



class ImageFile(BasicFile):
    exts = ("jpg", "png")
    sizes = (2048, 1024, 512, 256)
    def istype(self):
        if super(ImageFile, self).istype():
            if os.path.splitext(self.name)[1][1:].lower() in self.exts:
                return True
            if self.entry.is_dir() and self.getOrigFile():
                self.is_processed_folder = True
                return True
        return False

    def update(self):
        ret = [
            ["sizes", self.convert_sizes],
        ]
        return super(ImageFile, self).update(ret)

    def convert_sizes(self):
        if os.path.exists(os.path.join(self.getTargetFolder(), "256x.jpg")):
            return self.NO_CHANGE
        with TemporaryDirectory() as temp_dir:
            for s in self.sizes:
                run("convert {o} -resize {size}x{size}\\> {tmp}/{size}.jpg".format(size=s, tmp=temp_dir, **self.getRunOpts()))
                run("convert {o} -resize x{size}\\> {tmp}/x{size}.jpg".format(size=s, tmp=temp_dir, **self.getRunOpts()))
                run("convert {o} -resize {size}x\\> {tmp}/{size}x.jpg".format(size=s, tmp=temp_dir, **self.getRunOpts()))
            run("mv {td}/* {tf}".format(td=temp_dir, **self.getRunOpts()))
        return self.UPDATED

    def test_requirements():
        ret = True
        ret &= BasicFile.cmd_exists("convert")
        return ret
filetypes.append(ImageFile)



class VideoFile(BasicFile):
    exts = ("mkv", "mp4", "mts", "webm", "mpg", "mpeg")

    def istype(self):
        if super(VideoFile, self).istype():
            if os.path.splitext(self.name)[1][1:].lower() in self.exts:
                return True
            if self.entry.is_dir() and self.getOrigFile():
                self.is_processed_folder = True
                return True
        return False
            
    def update(self):
        ret = [
            ["multi", self.convert_multi_bitrates], # most important
            ["screenshot", self.convert_screenshots], # second important
            ["hls", self.convert_hls],
            ["dash", self.convert_dash],
            ["webm", self.convert_webm], # least important
            ["sprite", self.convert_sprite], # nice to have
        ]
        return super(VideoFile, self).update(ret)

    def convert_multi_bitrates(self):
        if os.path.exists(os.path.join(self.getTargetFolder(), "video_00500.mp4")):
            return self.NO_CHANGE
        with TemporaryDirectory() as temp_dir:
            try:
                run("python `which mp4-dash-encode.py` -v -b 3 -o {td}/v {o}".format(td=temp_dir, **self.getRunOpts()))
            except CalledProcessError:
                return self.ERROR
            run("mv {td}/v/video_* {tf}".format(td=temp_dir, **self.getRunOpts()))
        return self.UPDATED

    def convert_screenshots(self):
        if os.path.exists(os.path.join(self.getTargetFolder(), "img_3.jpg")):
            return self.NO_CHANGE
        with TemporaryDirectory() as temp_dir:
            d = self.getJson()
            duration = int(float(d["streams"][0]["duration"]))
            run("ffmpeg -i {o} -vf fps={fps}/{dur} {td}/img_%d.jpg".format(fps=5, dur=duration, td=temp_dir, **self.getRunOpts()))
            run("mv {td}/img_* {tf}".format(td=temp_dir, **self.getRunOpts()))
        return self.UPDATED

    def getJson(self):
        p = run("ffprobe -v quiet -print_format json -show_streams {tf}/{v}".format(v="video_00500.mp4", **self.getRunOpts()), universal_newlines=True, stdout=PIPE)
        return json.loads(p.stdout, strict=False)

    def convert_sprite(self):
        if os.path.exists(os.path.join(self.getTargetFolder(), "sprite.jpg")):
            return self.NO_CHANGE
        with TemporaryDirectory() as temp_dir:
            d = self.getJson()
            duration = int(float(d["streams"][0]["duration"]))
            run("ffmpeg -i {o} -vf fps={fps}/{dur} {td}/sprite_%d.jpg".format(td=temp_dir, fps=10, dur=duration, **self.getRunOpts()))
            for i in range(1,11):
                run("convert {td}/sprite_{i}.jpg -resize {size}x\\> {td}/sprite_{size}_{i}.jpg".format(i=i, size=256, td=temp_dir))
            run("montage {tmp}/sprite_{size}_* -tile 10x1 -geometry 256x {tmp}/sprite.jpg".format(size=256, tmp=temp_dir))
            run("mv {td}/sprite.jpg {tf}".format(td=temp_dir, **self.getRunOpts()))
        return self.UPDATED

    def convert_webm(self):
        if os.path.exists(os.path.join(self.getTargetFolder(), "video.webm")):
            return self.NO_CHANGE
        with TemporaryDirectory() as temp_dir:
            run("ffmpeg -i {o} -speed 1 -c:v libvpx -b:v 1M -c:a libvorbis -vf \"scale='min(600,iw)':-1\" {td}/video.webm".format(td=temp_dir, **self.getRunOpts()))
            run("mv {td}/video.webm {tf}".format(td=temp_dir, **self.getRunOpts()))
        return self.UPDATED

    def convert_dash(self):
        if os.path.exists(os.path.join(self.getTargetFolder(), "stream.mpd")):
            return self.NO_CHANGE
        with TemporaryDirectory() as temp_dir:
            run("mp4dash -o {t}/dash {tf}/video_0*.mp4".format(t=temp_dir, **self.getRunOpts()))
            run("mv {td}/dash/* {tf}".format(td=temp_dir, **self.getRunOpts()))
        return self.UPDATED

    def convert_hls(self):
        if os.path.exists(os.path.join(self.getTargetFolder(), "master.m3u8")):
            return self.NO_CHANGE
        with TemporaryDirectory() as temp_dir:
            run("mp4hls -o {t}/hls {tf}/video_0*.mp4".format(t=temp_dir, **self.getRunOpts()))
            run("mv {td}/hls/* {tf}".format(td=temp_dir, **self.getRunOpts()))
        return self.UPDATED

    def test_requirements():
        ret = True
        ret &= BasicFile.cmd_exists("python2.7")
        ret &= BasicFile.cmd_exists("mp4dash") #bento4
        ret &= BasicFile.cmd_exists("mp4-dash-encode.py") #bento4
        ffmpeg = BasicFile.cmd_exists("ffmpeg")
        ret &= ffmpeg
        ret &= BasicFile.cmd_exists("montage") #imagemagick
        if ffmpeg:
            v = run("ffmpeg -version", stdout=PIPE)
            opts = [
                b"--enable-libx264", # video for mp4
                b"--enable-libfdk-aac", # audio for mp4
                b"--enable-libvpx", # video for webm
                b"--enable-libvorbis", # audio for webm
            ]
            opts_not_exist = [o for o in opts if o not in v.stdout]
            if len(opts_not_exist) > 0:
                log.error("ffmpeg not compiled with {}".format(" ".join(opts_not_exist)))
                ret = False
        return ret
filetypes.append(VideoFile)
