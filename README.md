# web_video
Tool to encode videos inside a folder for the web, and small example how to display it


## Installation

Software:
```
python2.7 # for bento4
python3.5 # for this script
bento4    # for converting the videos
ffmpeg    # bento4 depends on ffmpeg
	- libfdk_aac # ffmpeg must be compiled with this
		# (brew install ffmpeg --with-fdk-aac --with-libvpx --with-libvorbis)
	- x264
imagemagick # for converting the images
```
You need python 2.7 and python 3.5
`pip3.5 install --user -r requirements.txt`

When installing (bento4)[https://www.bento4.com/] add it to your PATH like this:
```
	export PATH="${PATH}:/xyz/Bento4-SDK-1-5-0-613.x86_64-unknown-linux/bin"
	export PATH="${PATH}:/xyz/Bento4-SDK-1-5-0-613.x86_64-unknown-linux/utils"
```

## Usage

call `run.py folder http://callback-url`
The folder should contain folders with video files inside

E.g.
```
folder/my_album1/vid.mp4
folder/my_album1/test.jpg
folder/another/abc.mp4
```

After running it looks like this:
```
folder/my_album1/vid/
                     master.m3u8
                     stream.mpd
                     video_00500.mp4
                     video_01250.mp4
                     video_02000.mp4
                     ...
folder/my_album1/test/
                      2048.jpg
                      1024.jpg
                      512.jpg
                      256.jpg
folder/another/abc/
                   master.m3u8
                   stream.mpd
                   video_00500.mp4
                   video_01250.mp4
                   video_02000.mp4
                   ...
```

It will call the `callback-url 2 times` (once per album).


## Example
Look into `web` there is a folder `galleries` which can be converted by: `./web_video/run.py web/galleries`. Then you can
`cd web; php -S localhost:8000` and browse to http://127.0.0.1:8000.

# Composer

Maybe you want to use the classes Gallery and Element in your project - so you can composer require them.
```
composer require balrok/web_video dev-master
```
And use it with
```
use balrok\web_video\web\Gallery;
use balrok\web_video\web\Element;
```
