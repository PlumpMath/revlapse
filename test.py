from pytineye import TinEyeAPIRequest
from contextlib import closing

global api

def initAPI():
	global api
	api = TinEyeAPIRequest('http://api.tineye.com/rest/', 'your_public_key', 'your_private_key')
#	print api.remaining_searches()

def reverseSearch(image, count=1):
	global api
	with closing(open(image, 'rb')) as fp:
		data = fp.read()
		#resp = api.search_data(data=data)
		print( resp.matches )

		
def main():
	initAPI()
	#print reverseSearch('imgs/example1.jpg')
