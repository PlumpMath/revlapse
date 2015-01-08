#!/usr/bin/python

from subprocess import call
import youtube_dl
import urlparse
import os
from os import listdir
from os.path import isfile, join
from fnmatch import fnmatch
import urllib2
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


VIDEODIR = 'videos/'
VIDEORAWDIR = 'videos/raws/'
FRAMESDIR = 'videos/frames/'
GRISDIR = 'videos/grisframes/'
GRISMOVIEDIR = 'videos/grisvideo/'

WEB_PREFIX = "http://vps.provolot.com/GITHUB/revlapse/"

VIDEO_URL = "https://www.youtube.com/watch?v=KJKC3cwv5b0"
VIDEO_URL = "https://www.youtube.com/watch?v=TxTeUNygQd0"
#VIDEO_URL = "https://www.youtube.com/watch?v=GOAEIMx39-w"
VIDEO_URL = "https://www.youtube.com/watch?v=v_4ghLXaEVM"
VIDEO_URL = 'http://www.youtube.com/watch?v=BaW_jenozKc'
VIDEO_URL = "https://www.youtube.com/watch?v=ij-4nz6Bo0U"
VIDEO_URL = "https://www.youtube.com/watch?v=L6Wo4MZtnGI"

FPS = "10"
NUMFRAMES = 0

ydl_opts = {
	'outtmpl': VIDEORAWDIR + '%(id)s.%(ext)s',
	'logger': MyLogger(),
#	'progress_hooks': [my_hook],
}

def getFrameFiles(ytfilename, directory):
    frameFiles = [ f for f in listdir(directory) if isfile(join(directory,f)) and fnmatch(f, ytfilename + '*')]
    frameFiles.sort()
    return frameFiles


YTFRAMESDIR = ""
YTGRISFRAMESDIR = ""


def getYTVideo():
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        # DOWNLOAD YOUTUBE VIDEO
        ydl.download([VIDEO_URL])

 
def getYTImages():
   # GET FRAMES FROM VIDEO"
    YTFRAMESDIR = FRAMESDIR + ytfilename + "/"
    if not os.path.exists(YTFRAMESDIR):
            os.makedirs(YTFRAMESDIR)

    ffmpegCallPrev = ["ffmpeg", "-i", VIDEORAWDIR + ytfilename, "-r", FPS] 
    ffmpegFrameTemplate = [YTFRAMESDIR + ytfilename + "_frame_%5d.jpg"]

    if(NUMFRAMES != 0):
            ffmpegCall = ffmpegCallPrev + ["-vframes", str(NUMFRAMES)] + ffmpegFrameTemplate
    else:
            ffmpegCall = ffmpegCallPrev + ffmpegFrameTemplate
    print ffmpegCall
    call(ffmpegCall)



def getGrisImages():
    YTFRAMESDIR = FRAMESDIR + ytfilename + "/"
    YTGRISFRAMESDIR = GRISDIR + ytfilename + "/"
    if not os.path.exists(YTGRISFRAMESDIR):
            os.makedirs(YTGRISFRAMESDIR)
    frameFiles = getFrameFiles(ytfilename, YTFRAMESDIR)
    # this is not a map because getGrisImage takes a loooong time
    GrisFiles = []
    for i, frame in enumerate(frameFiles):
            print "=== FRAME: ", WEB_PREFIX + YTFRAMESDIR + frame
            try:
                fGrisDict = googleGris.getGrisImage(WEB_PREFIX + YTFRAMESDIR + frame, minArea=150000, imageOnly=False)
                
                if(fGrisDict):
                        fGris = fGrisDict[u'ou']
                        fGrisRef = fGrisDict[u'ru']
                        print "=== GRISFRAME: ", fGris
                        GrisFiles.append({ "index" : i, "framename" : frame, "frameGrisname" : fGris})
                        try:
                            req = urllib2.Request(fGris)
                            req.add_header('Referer', fGrisRef)
                            r = urllib2.urlopen(req)
                            img = r.read()
                            open(YTGRISFRAMESDIR + frame, 'wb').write(img)
                            print "=== GRISFRAME DOWNLOADED"
                        except Exception, e:
                            print e
                            print "=== GRISFRAME ERROR DOWNLOADING"
                else:
                        print "=== GRISFRAME NONEXISTENT"
            except Exception, e:
                print e





def compositeGrisVideo():
    GRISMOVIEOUT = GRISMOVIEDIR + ytfilename + ".mp4"
    grisFrameTemplate = YTGRISFRAMESDIR + ytfilename + "_frame_%5d.jpg"
    grisFrameTemplate = GRISDIR + "L6Wo4MZtnGI.mp4" + "/" + "L6Wo4MZtnGI.mp4" + "_frame_%*.jpg"
    print grisFrameTemplate

    ffmpegCompositeCall = ["ffmpeg", "-framerate", str(FPS), "-i", grisFrameTemplate, "-c:v", "libx264", "-r", "30", "-pix_fmt", "yuv420p", "-s", "720x480", GRISMOVIEOUT, "-y"]
    print " ".join(ffmpegCompositeCall)
    call(ffmpegCompositeCall)



def main():
	global ytfilename
	global YTFRAMESDIR, YTGRISFRAMESDIR
	ytfilename = None

        ytfilename = VIDEO_URL.split("=")[1] + ".mp4"

        """
        print "\n\n======"
        print "Downloading youtube video " + VIDEO_URL
        getYTVideo()
        
        print "\n\n======"
        print "Downloading youtube images " + VIDEO_URL
        getYTImages()
        
        print "\n\n======"
        print "Frames obtained: doing Reverse Image Search and downloading"
        GrisFiles = getGrisImages()

        if(len(GrisFiles) == 0):
            return -1
        """
        print "\n\n======"
        print "Reverse Image Frames obtained: compositing"
        compositeGrisVideo()

        for rf in GrisFiles:
                print json.dumps(rf, indent=4)

if __name__ == "__main__":
    main()

