import csv
import indicoio
import operator
from time import time
import tweepy #https://github.com/tweepy/tweepy
import os.path
#Twitter API credentials
personality =  {'conscientiousness': 0, 'openness': 0, 'agreeableness': 0, 'extraversion':0}
consumer_key = ""
consumer_secret = ""
access_key = ""
access_secret = ""
indicoio.config.api_key = 'a70776a16ea44fe661bbb0e2aaec1e12'
data = []


def get_all_tweets(screen_name):
	global consumer_key, consumer_secret, access_key, access_secret
	#Twitter only allows access to a users most recent 3240 tweets with this method
	
	#authorize twitter, initialize tweepy
	auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
	auth.set_access_token(access_key, access_secret)
	api = tweepy.API(auth)
	
	#initialize a list to hold all the tweepy Tweets
	alltweets = []	
	
	#make initial request for most recent tweets (200 is the maximum allowed count)
	new_tweets = api.user_timeline(screen_name = screen_name,count=100)
	
	#save most recent tweets
	alltweets.extend(new_tweets)
	
	#save the id of the oldest tweet less one
	oldest = alltweets[-1].id - 1
	
	#keep grabbing tweets until there are no tweets left to grab
	#while len(new_tweets) > 0:
		#print("getting tweets before {}".format(oldest))
		
		#all subsiquent requests use the max_id param to prevent duplicates
	new_tweets = api.user_timeline(screen_name = screen_name,count=200,max_id=oldest)
		
		#save most recent tweets
	alltweets.extend(new_tweets)
		
		#update the id of the oldest tweet less one
	oldest = alltweets[-1].id - 1
		
		#print("...{} tweets downloaded so far".format(len(alltweets)))
	
	#transform the tweepy tweets into a 2D array that will populate the csv	
	outtweets = [[bytes(tweet.id_str,"utf-8"),
                      tweet.created_at,
                      bytes(tweet.text,"utf-8")] for tweet in alltweets]
	#print(type(outtweets))
	
	#write the csv	
	with open('%s_tweets.csv' % screen_name, 'w') as f:
		writer = csv.writer(f)
		writer.writerow(["id","created_at","text"])
		writer.writerows(outtweets)


def cons():
	global personality 
	personality["conscientiousness"] += 1
	#print("in")

def ope():
	global personality
	personality["openness"] += 1
	#print("in")

def agr():
	global personality
	personality["agreeableness"] += 1
	#print("in")

def extra():
	global personality
	personality["extraversion"] += 1
	#print("in")
def clear():
	global personality
	personality["extraversion"] = 0
	personality["conscientiousness"] = 0
	personality["openness"] = 0
	personality["agreeableness"] = 0

# After opened, run this code:

#print_count = 0
def main_func(name):
	global data, personality
	csv_name = name + '_tweets.csv'
	if not os.path.isfile(csv_name):
		get_all_tweets(name)
	with open(csv_name) as file:
		reader = csv.reader(file)
		count = 0
		for row in reader:
			if len(row) > 0:
				text = row[2][2:-1]
				#print(text)
				if "https" in text:
					continue

				data.append(text)
				count +=1
			if count > 10:
				break
				

	 
	options = {'conscientiousness': cons, 'openness': ope, 'agreeableness': agr, 'extraversion':extra}

	t0= time()
	for i in data:
		
		mini_dic = indicoio.personality(i)
		
		result = max(mini_dic.keys(), key=(lambda k: mini_dic[k]))
		if result in options:
			options[result]()
		else:
			pass

	the_personality = max(personality.keys(), key=(lambda k: personality[k]))
	clear()
	return the_personality



# Call main func
