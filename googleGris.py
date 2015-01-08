import json
import urllib2
import requests
import random
import operator


def blockspringGris(image_url):
	req = urllib2.Request("https://sender.blockspring.com/api_v2/blocks/4521f0eb2b5658d71ab4cf25a7af0a0c?api_key=947b009aeaa33b92c20db3012884c3de")
	req.add_header('Content-Type', 'application/json')
	data = {"image_url": image_url}
	results = urllib2.urlopen(req, json.dumps(data)).read()
	return json.loads(results)

def getGrisImage(image_url, pickRandom=True, imageOnly=True, minArea=0):
	similars = blockspringGris(image_url)[u'visually_similar_images']
       # print similars
	if(len(similars) == 0):
		return None

        if(minArea == 0):
            if(pickRandom):
                    imgpick = random.choice(similars)
            else:
                    imgpick = similars[0]

            if(imageOnly):
                    return imgpick[u'ou']
            else:
                    return imgpick

        def addArea(d):
            d['oarea'] = int(d[u'ow']) * int(d[u'oh'])
            return d
        similars = map(addArea, similars)
        similars = sorted(similars, key=lambda d: d['oarea'], reverse=True) 
        bigEnoughSims = filter(lambda d: d['oarea'] >= minArea, similars)
        notBigEnoughSims = filter(lambda d: d['oarea'] < minArea, similars)

        if(len(bigEnoughSims) >= 1):
            if(pickRandom):
                    imgpick = random.choice(bigEnoughSims)
            else:
                    imgpick = bigEnoughSims[0]

            if(imageOnly):
                    return imgpick[u'ou']
            else:
                    return imgpick

        else:
            if(len(notBigEnoughSims) >= 1):
				if(imageOnly):
					return notBigEnoughSims[0][u'ou']
				else:
					return notBigEnoughSims[0]
            else:
                return None

def main():
	print getGrisImage("http://vps.provolot.com/GITHUB/revlapse/imgs/example1.jpg")

if __name__ == "__main__":
	main()


