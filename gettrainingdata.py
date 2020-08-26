from twarc import Twarc

tw = Twarc()
#get training data
for tweet in tw.search("covid-19", lang = 'en'):
	try:
		screen_name = None
		if "screen_name" in tweet["user"]:
			screen_name = tweet["user"]["screen_name"]
		id_str = tweet["id_str"]
		tweet_url = None
		if "id_str" != None and "screen_name" != None:
			tweet_url = "https://twitter.com/" + screen_name + "/status/" + id_str
		#put training data into a txt file
		with open("trainingcovid-19.txt", "a+") as f:
			# Move read cursor to the start of file.
			f.seek(0)
			# If file is not empty then append '\n'
			data = f.read(100)
			if len(data) > 0 :
				f.write("\n")
			# Append text at the end of file
			f.write(tweet['full_text'])
			f.write("\n")
			f.write(tweet_url)

	except UnicodeEncodeError:
		print("UnicodeEncodeError in finding training data")

#now we have to manually sort training data