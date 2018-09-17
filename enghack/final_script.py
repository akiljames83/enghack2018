'''
Creator: Akil Hamilton
Description: Script to determine a twitter user's personality based on their tweets. Subsequently, the script will use information from 
Waterloo Open Data to present to you events that would match up with your personality. The personality analysis of the Waterloo Open Data
is done before hand so as to reduce the computation time required to run the algoirthm on a new user's tweets. This script was created by 
me, however, I worked on the overall hack with Shahzada Khoso at EngHacks 2018 where he worked on the Front End and Back End Design.
This script has been Refactored for the HackNY application as the previous version was built in 24-hours. 
'''

import csv
import indicoio # Commercial Library for Machine Learning and Sentiment Analysis tools
import operator
import tweepy # https://github.com/tweepy/tweepy
import os.path
import threading
import datetime
import urllib.request

# API key for Inicoio sentiment analysis library
indicoio.config.api_key = ''

# Global counter of a persons personality based on their tweets
personality_dict =  {'conscientiousness': 0, 'openness': 0, 'agreeableness': 0, 'extraversion':0}

def initialize_events_by_personality():
	'''
	Function to scrape the most recent events from Waterloo Open Data and to use sentiment analysis 
	to determine the personality trait of the events based on the given description.
	'''
	now = datetime.datetime.now()
	event_info, all_events, event_names, processed = [], [], [], []

	# The personality that are posible due to sentiment analysis algorithm:
	coae = ["conscientiousness","openness","agreeableness","extraversion"]

	url = 'http://maps.waterloo.ca/OpenData/events.csv'
	with urllib.request.urlopen(url) as file:
		reader = csv.reader(file)
		next(reader)
		
		for index, row in enumerate(reader):
			# skips over empty rows of data
			if len(row) > 0: 
				# Clean up: Category, Event Description and Name that contain embedded html tags
				Category = row[5].replace('<p>', "").replace('</p>',"").replace("&quot","")
				Description = row[7].replace('<p>', "").replace('</p>',"").replace("&quot","")
				Name = row[13].replace('<p>', "").replace('</p>',"").replace("&quot","")

				# Clean up date information
				dateArr = row[2][:10].split("/")

				Month = int(dateArr[0])
				Day = int(dateArr[1])
				Year = int(dateArr[2])

				Date = (Day, Month, Year)

				# If the event has already occured, skip the event
				if not(Year>= now.year and Month>=now.month and Day>=now.day): 
					continue
				try:
					event_info.extend([name, category, description, Date])

					# If the event is already accunted for, clear small_list and go to ext row
					if name in event_names:
						event_info = []
						continue
					else:
						event_names.append(name)
						all_events.append(event_info)
						event_info = []

				except UnicodeEncodeError:
					pass

			# As this is a csv file, a stoping row should be specified or reader will iterate over empty rows
			if index > 600:
				break

	for event in all_events:
		try:
			if event[2] == '': # if no description is present
				continue

			# Use sentiment analysis to determine personality of event
			mini_dic = indicoio.personality(str(event[2]))
			result = max(mini_dic.keys(), key=(lambda k: mini_dic[k]))

			# _ -> eventName, emotion, type of event, description, date tuple(day month year)
			_ = (event[0], result, event[1], event[2], event[3])
			processed.append(_)

		except UnicodeEncodeError:
			pass

	def createCSV():
		name = coae.pop(-1)
		label = name + ".csv"
		# Create for CSV files containing the events corresponding to the personality types
		with open(label,'w',newline = '') as f:
			thewriter = csv.writer(f)
			thewriter.writerow(["Event Name", "Personality Type", "Type of Event", "Description","Day","Month","Year"])
			for row in processed:
				if row[1] == name:
					thewriter.writerow([row[0],row[1],row[2],row[3],row[4][0], row[4][1], row[4][2]])

	# Initialize threads to create an events CSV file for each personality
	t1 = threading.Thread(name='con', target=createCSV)
	t2 = threading.Thread(name='open', target=createCSV)
	t3 = threading.Thread(name='agre', target=createCSV)
	t4 = threading.Thread(name='extra', target=createCSV)

	threads = [t1] + [t2] + [t3] + [t4]

	for x in threads:
		x.start()

	for x in threads:
		x.join()


def get_all_tweets(screen_name,num_tweets=200):
	'''
	screen_name::type -> [str]
	num_tweets::type -> [int]
	Function to get X most recent tweets of user.
	num_tweets is capped at 200 tweets as twitter api only allows scrapping of most recent 200 tweets
	at a time. Additionally, more than this number would make script take very long to run.
	'''
	if num_tweets > 200: num_tweets = 200
	#Twitter API credentials
	consumer_key, consumer_secret, access_key, access_secret = '' '' '', ''
	
	#authorize twitter, initialize tweepy
	auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
	auth.set_access_token(access_key, access_secret)
	api = tweepy.API(auth)
	
	#initialize a list to hold all the tweepy Tweets
	alltweets = []	
	
	#make initial request for most recent tweets (200 is the maximum allowed count)
	new_tweets = api.user_timeline(screen_name = screen_name,count=num_tweets)
	
	#save most recent tweets
	alltweets.extend(new_tweets)
	
	#transform the tweepy tweets into a 2D array that will populate the csv	
	outtweets = [[bytes(tweet.id_str,"utf-8"),
                      tweet.created_at,
                      bytes(tweet.text,"utf-8")] for tweet in alltweets]
	
	#write the csv	
	with open('%s_tweets.csv' % screen_name, 'w') as f:
		writer = csv.writer(f)
		writer.writerow(["id","created_at","text"])
		writer.writerows(outtweets)

# Main Script
def analyze_personality(twitter_name):
	'''
	twitter_name::type -> [str]
	Function to determine the personality of user base on a csv file containing their most recent tweets.
	'''
	global personality_dict
	data = []

	csv_name = twitter_name + '_tweets.csv'
	if not os.path.isfile(csv_name):
		get_all_tweets(twitter_name)

	with open(csv_name) as file:
		reader = csv.reader(file)
		for row in reader:
			if len(row) > 0:
				# checks if the content of the tweet is a link to an article/image
				text = row[2][2:-1]
				if "https" in text:
					continue
				data.append(text)

	coae = ["conscientiousness","openness","agreeableness","extraversion"]

	for i in data:
		mini_dic = indicoio.personality(i)
		result = max(mini_dic.keys(), key=(lambda k: mini_dic[k]))
		if result in coae:
			increment_personality(result)

	personality = max(personality_dict.keys(), key=(lambda k: personality_dict[k]))
	clear(coae)
	return personality

# Main Script Helper Functions
def increment_personality(result):
	'''
	result::type -> [str]
	Function to increment the personality count of user based on current tweet
	'''
	global personality_dict
	personality_dict[result] += 1

def clear(coae):
	'''
	coae::type -> arr[str]
	Function to clear the personality dictionary once all tweets have been iterated through for user
	'''
	global personality_dict
	for personality in coae:
		personality_dict[personality] = 0

if __name__ == "__main__":
	# Putting everything together to determine a person's personality

	# Create 4 CSV files, each containing events based on a person's personality trait
	initialize_events_by_personality()

	# Retrieve user's twitter name
	twitter_name = input("What is ur twitter username?")

	# Determine User's Personality
	personality = analyze_personality(twitter_name)
	print('Your personality trait is %s and you can find events in Waterloo based on your personality in "%s"!' % (personality, (personality + ".csv")))

	# When we submitted this idea for the hackathon, we created a user interface as well that found a picture related to the event and using flask on 
	# backend we randomly displayed 5 events relating to the users personality. I focused on the development on the script primarily while my teamate worked on user
	# interface and some of the backend scripting. Finally, we used the indicoio API for sentiment analysis as it was provided in the hack, however, it would be
	# very possible to use tensorflow and create a RNN to determine a users personality given a tweet.

	# An extended overview of our project can be found at: https://devpost.com/software/socialoo

	# The demo provided on the devpost link does not include the refactored front end design that I worked on but it shows how our script works!