import json
import urllib2
import requests
import random

def blockspringGris(image_url):
	req = urllib2.Request("https://sender.blockspring.com/api_v2/blocks/4521f0eb2b5658d71ab4cf25a7af0a0c?api_key=947b009aeaa33b92c20db3012884c3de")
	req.add_header('Content-Type', 'application/json')
	data = {"image_url": image_url}
	results = urllib2.urlopen(req, json.dumps(data)).read()
	return json.loads(results)

def getGrisImage(image_url, pickRandom=True):
	similars = blockspringGris(image_url)[u'visually_similar_images']
	if(len(similars) == 0):
		return None
	if(pickRandom):
		imgpick = random.choice(similars)
	else:
		imgpick = similars[0]
	return imgpick[u'ou']


def main():
	print getGrisImage("http://vps.provolot.com/GITHUB/revlapse/imgs/example1.jpg")

if __name__ == "__main__":
	main()


