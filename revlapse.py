from subprocess import call
import youtube_dl
import os

class MyLogger(object):
	def debug(self, msg):
		pass

	def warning(self, msg):
		pass

	def error(self, msg):
		print(msg)


def my_hook(d):
	global ytfilename
	if d['status'] == 'finished':
		print('Done downloading, now converting ...')
	if not(ytfilename):
		ytfilename = os.path.basename(d['filename'])

VIDEODIR = 'videos/raws/'
FRAMESDIR = 'videos/frames/'

ydl_opts = {
	'outtmpl': VIDEODIR + '%(id)s.%(ext)s',
	'logger': MyLogger(),
	'progress_hooks': [my_hook],
}

global ytfilename
ytfilename = None

#VIDEO_URL = "https://www.youtube.com/watch?v=KJKC3cwv5b0"
VIDEO_URL = 'http://www.youtube.com/watch?v=BaW_jenozKc'
FPS = "0.1"

with youtube_dl.YoutubeDL(ydl_opts) as ydl:
	ydl.download([VIDEO_URL])
	print ytfilename
	call(["ffmpeg", "-i", VIDEODIR + ytfilename, "-r", FPS, FRAMESDIR + ytfilename + "_frame_%3d.jpg"])
