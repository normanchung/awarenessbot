from twarc import Twarc
import numpy


def training():
	#this is where we train using the training data, bag of words model
	dictpos = {}
	dictneg = {}
	counterpos = 0
	counterneg = 0
	a = 0.01

	with open("trainingcovid-19.txt",'r', encoding="utf-8") as file:
		for line in file:
			try:
				
				if(not line.startswith('https://twitter.com')):
					lastword = line.split()
					classdef = lastword[-1]
					if (classdef == ',1'):
						for eachword in lastword[0:len(lastword) - 1]:
							if eachword in dictpos:
								dictpos[eachword]['count'] += 1
								counterpos += 1
							else:
								dictpos[eachword] = {'count': 1.0, 'probability': 0.0}
								counterpos += 1

					elif (classdef == ',0'):
						for eachword in lastword[0:len(lastword) - 1]:
							if eachword in dictneg:
								dictneg[eachword]['count'] += 1
								counterneg += 1
							else:
								dictneg[eachword] = {'count': 1.0, 'probability': 0.0}
								counterneg += 1

			except UnicodeDecodeError:
				print("UnicodeDecodeError in training algorithm")

	#calculating the probability for each word in the dictionary
	for eachword in dictpos:
		dictpos[eachword]['probability'] = (dictpos[eachword]['count'] + a) / (counterpos + (a * (counterpos + counterneg)))

	for eachword in dictneg:
		dictneg[eachword]['probability'] = (dictneg[eachword]['count'] + a) / (counterneg + (a * (counterpos + counterneg)))

	return dictpos, dictneg, counterpos, counterneg, a


def gettestingdata():
	#get testing data to be tested on into txt file, used popular tweets
	for tweet in tw.search("covid-19", lang = 'en', result_type = 'popular'):
		try:

			screen_name = None
			if "screen_name" in tweet["user"]:
				screen_name = tweet["user"]["screen_name"]
			id_str = tweet["id_str"]
			tweet_url = None
			if "id_str" != None and "screen_name" != None:
				tweet_url = "https://twitter.com/" + screen_name + "/status/" + id_str

			with open("testingcovid-19.txt", "a+") as f:
				f.seek(0)
				data = f.read(100)
				if len(data) > 0 :
					f.write("\n")
				f.write(tweet['full_text'])
				f.write("\n")
				f.write(tweet_url)

		except UnicodeEncodeError:
			print("UnicodeEncodeError in finding popular tweets")


def testing(dictpos, dictneg, counterpos, counterneg, a):
	#test using the testing data
	positive = False
	with open("testingcovid-19.txt",'r') as file:
		for line in file:
			try:
				#if the previous line is a good tweet, then save the url for the tweet in the txt file
				if(line.startswith('https://twitter.com') and positive == True):
					with open("testingcovid-19result.txt", "a+") as f:
						f.seek(0)
						data = f.read(100)
						if len(data) > 0 :
							f.write("\n")
						f.write(line)
					positive = False

				else:
					#testing each tweet to determine whether tweet is good or not
					testpos = 0.0
					testneg = 0.0
					withoutclass = line.split()
					for eachword in withoutclass:
						if eachword in dictpos:
							testpos += numpy.log10(dictpos[eachword]['probability'])
						else:
							testpos += numpy.log10(a / (counterpos + (a * (counterpos + counterneg))))
						if eachword in dictneg:
							testneg += numpy.log10(dictneg[eachword]['probability'])
						else:
							testneg += numpy.log10(a / (counterneg + (a * (counterpos + counterneg))))
					#if it's good, write it into the result txt file
					if (testpos > testneg):
						with open("testingcovid-19result.txt", "a+") as f:
							f.seek(0)
							data = f.read(100)
							if len(data) > 0 :
								f.write("\n")
							f.write(line)
							positive = True

			except UnicodeEncodeError:
				print("UnicodeEncodeError in testing data")


if __name__ == '__main__':
	tw = Twarc()
	dictpos, dictneg, counterpos, counterneg, a = training()
	gettestingdata()
	testing(dictpos, dictneg, counterpos, counterneg, a)
