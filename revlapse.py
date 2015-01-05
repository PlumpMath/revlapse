#!/usr/bin/python

from subprocess import call
import youtube_dl
import urlparse
import os
from os import listdir
from os.path import isfile, join
from fnmatch import fnmatch
import urllib
import googleGris
import json

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
GRISDIR = 'videos/grisframes/'

WEB_PREFIX = "http://vps.provolot.com/GITHUB/revlapse/"

VIDEO_URL = "https://www.youtube.com/watch?v=KJKC3cwv5b0"
#VIDEO_URL = 'http://www.youtube.com/watch?v=BaW_jenozKc'
VIDEO_URL = "https://www.youtube.com/watch?v=TxTeUNygQd0"
VIDEO_URL = "https://www.youtube.com/watch?v=ij-4nz6Bo0U"
VIDEO_URL = "https://www.youtube.com/watch?v=v_4ghLXaEVM"
VIDEO_URL = "https://www.youtube.com/watch?v=L6Wo4MZtnGI"


FPS = "1"
NUMFRAMES = 15 


ydl_opts = {
	'outtmpl': VIDEODIR + '%(id)s.%(ext)s',
	'logger': MyLogger(),
	'progress_hooks': [my_hook],
}

global ytfilename
ytfilename = None

def getFrameFiles(ytfilename):
	frameFiles = [ f for f in listdir(FRAMESDIR) if isfile(join(FRAMESDIR,f)) and fnmatch(f, ytfilename +'_*')]
        frameFiles.sort()
	return frameFiles




with youtube_dl.YoutubeDL(ydl_opts) as ydl:

	# DOWNLOAD YOUTUBE VIDEO
	ydl.download([VIDEO_URL])

	# GET FRAMES FROM VIDEO
	YTFRAMESDIR = FRAMESDIR + ytfilename + "/"
	if not os.path.exists(YTFRAMESDIR)
		os.makedirs(YTFRAMESDIR)

	ffmpegCallPrev = ["ffmpeg", "-i", VIDEODIR + ytfilename, "-r", FPS] 
	ffmpegFrameTemplate = [YTFRAMESDIR + ytfilename + "_frame_%3d.jpg"]
	if(NUMFRAMES != 0):
		ffmpegCall = ffmpegCallPrev + ["-vframes", str(NUMFRAMES)] + ffmpegFrameTemplate
	else:
		ffmpegCall = ffmpegCallPrev + ffmpegFrameTemplate
	print ffmpegCall

	call(ffmpegCall)

	# GET GRIS FRAMES
	
	YTGRISFRAMESDIR = GRISFRAMESDIR + ytfilename + "/"
	if not os.path.exists(YTGRISFRAMESDIR)
		os.makedirs(YTGRISFRAMESDIR)

	frameFiles = getFrameFiles(ytfilename)
	print "\n\n======"
	print "Frames obtained: doing Reverse Image Search and downloading"
	# this is not a map because getGrisImage takes a loooong time
	RisFiles = []
	for i, frame in enumerate(frameFiles):
		print "=== FRAME: ", WEB_PREFIX + YTFRAMESDIR + frame
		fGris = googleGris.getGrisImage(WEB_PREFIX + YTFRAMESDIR + frame, minArea=150000)
                if(fGris != "-1"):
			print "=== GRISFRAME: ", fGris
			RisFiles.append({ "index" : i, "framename" : frame, "frameGrisname" : fGris})
			urllib.urlretrieve(fGris, YTGRISFRAMEDIR + frame)
			print "=== GRISFRAME DOWNLOADED"
		else:
			print "=== GRISFRAME NONEXISTENT"

	for rf in RisFiles:
		print json.dumps(rf, indent=4)

