#!/usr/bin/python
import os
import revlapse

ytprefix = revlapse.VIDEO_URL.split("?v=")[1]
YTFRAMESDIR = revlapse.FRAMESDIR + ytprefix + ".mp4/"
YTGRISFRAMESDIR = revlapse.GRISDIR + ytprefix + ".mp4/"

frameFilenames = revlapse.getFrameFiles(ytprefix, YTFRAMESDIR)
frameFilepaths = map(lambda x: YTFRAMESDIR + os.path.basename(x), frameFilenames)
grisFrameFilepaths = map(lambda x: YTGRISFRAMESDIR + os.path.basename(x), frameFilenames)

framePairs = zip(frameFilepaths, grisFrameFilepaths)

with open(revlapse.VIDEODIR + ytprefix + '_compare.html', 'w') as fp:
    fp.write("<html><body><table style=width:100%>\n")
    fp.write('<link rel="stylesheet" type="text/css" href="style.css">\n')

    for framep in framePairs:
        fp.write("<tr>\n")
        fp.write("<td class='orig'>")
        fp.write("<img src='" + revlapse.WEB_PREFIX + framep[0] + "'>")
        fp.write("</td>\n")
        fp.write("<td class='gris'>")
        fp.write("<img src='" + revlapse.WEB_PREFIX + framep[1] + "'>")
        fp.write("</td>\n")
        fp.write("</tr>\n")

    fp.write("</table></body></html>\n")

