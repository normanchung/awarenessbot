from twarc import Twarc
import numpy
import requests
import urllib.request
import os
import facebook


def embedding():
	#take each tweet and get the html format of tweet into another txt file
	with open("testingcovid-19result.txt",'r') as file:
		for line in file:
			try:

				if(line.startswith('https://twitter.com')):
					with open("resultshtml.txt", "a+") as f:
						f.seek(0)
						data = f.read(100)
						if len(data) > 0 :
							f.write("\n")
						f.write(tw.oembed(line)['html'])

			except UnicodeEncodeError:
				print("UnicodeEncodeError in printing HTML")


def createimageurl():
	#create an image from the html of tweet using HCTI, and save the url of the created image
	HCTI_API_ENDPOINT = "https://hcti.io/v1/image"
	#Retrieve these from https://htmlcsstoimage.com/dashboard
	HCTI_API_USER_ID = ''
	HCTI_API_KEY = ''
	with open("resultshtml.txt",'r') as file:
		for line in file:
			if(line.startswith('<blockquote')):
				fullline = line
			if(line.startswith('<script')):
				fullline += line
				data = {'html': fullline}
				image = requests.post(url = HCTI_API_ENDPOINT, data = data, auth=(HCTI_API_USER_ID, HCTI_API_KEY))
				
				with open("imageurl.txt", "a+") as f:
						f.seek(0)
						data = f.read(100)
						if len(data) > 0 :
							f.write("\n")
						f.write(image.json()['url'])


def urltoimage():
	#given all image urls, save them locally
	with open('imageurl.txt', 'r') as file:
		for line in file:
			i = 0
			while os.path.exists('covid-19_%s.jpg' % i):
				i += 1
			r = requests.get(line.strip())
			with open('covid-19_%s.jpg' % i, 'wb') as outfile:
				outfile.write(r.content)


def postingonfb():
	#given the image, and the tweet url, now we post on a facebook page called Covid-19 Awareness
	graph = facebook.GraphAPI(access_token='', version="3.0")
	with open("testingcovid-19result.txt",'r') as file:
		for line in file:
			try:

				if(line.startswith('https://twitter.com')):
					#Upload an image with a caption.
					i = 0
					while os.path.exists('covid-19_%s.jpg' % i):
						i += 1
					graph.put_photo(image=open('covid-19_%s.jpg' % i, 'rb'), caption=line)

			except UnicodeEncodeError:
				print("UnicodeEncodeError in making caption")


if __name__ == '__main__':
	tw = Twarc()
	embedding()
	createimageurl()
	urltoimage()
	postingonfb()
