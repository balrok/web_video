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


## PHP script
Using flowplayer works but it has some quirks. The javascript part of the PHP-script works a little bit around them.
Maybe you also have a better idea for this

Also added my crossdomain.xml - this is required for HLS and DASH and save you a google-search

## TODO

* add a small example here folder with some imgs and videos to easily check if it works
