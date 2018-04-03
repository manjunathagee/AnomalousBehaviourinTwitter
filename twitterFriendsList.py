#!/usr/bin/python

#-----------------------------------------------------------------------
# twitter-friends
#  - lists all of a given user's friends (ie, followees)
#-----------------------------------------------------------------------

from twitter import *
import tweepy #https://github.com/tweepy/tweepy
import csv

#-----------------------------------------------------------------------
#Twitter API credentials
consumer_key = "BxBdlEvlJizyyDqD5U8T5wrCX"
consumer_secret = "nY1827gmZ38AviFvTSLQTXy5ppY5U8czkADE6Q5Ww9vwA8cfRG"
access_key = "1057279068-3t4a1VJWdOug4e5ZkgDIp1mAqfJP2GmJbPHtAiF"
access_secret = "WmKaFJBpxEJ75zT2kf15fIAZMPObZIObtNaO4ifCsDtee"

#-----------------------------------------------------------------------

#-----------------------------------------------------------------------
# Utility function which will extract create and dumps user's info in cvs file
def get_all_tweets(screen_name):
    #Twitter only allows access to a users most recent 3240 tweets with this method
    
    #authorize twitter, initialize tweepy
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_key, access_secret)
    api = tweepy.API(auth)
    
    #initialize a list to hold all the tweepy Tweets
    alltweets = []    
    
    #make initial request for most recent tweets (200 is the maximum allowed count)
    new_tweets = api.user_timeline(screen_name = screen_name,count=200)
    
    #save most recent tweets
    alltweets.extend(new_tweets)
    
    #save the id of the oldest tweet less one
    oldest = alltweets[-1].id - 1
    
    #keep grabbing tweets until there are no tweets left to grab
    while len(new_tweets) > 0:
        print "getting tweets before %s" % (oldest)
        
        #all subsequent requests use the max_id param to prevent duplicates
        new_tweets = api.user_timeline(screen_name = screen_name,count=200,max_id=oldest)
        
        #save most recent tweets
        alltweets.extend(new_tweets)
        
        #update the id of the oldest tweet less one
        oldest = alltweets[-1].id - 1
        
        print "...%s tweets downloaded so far" % (len(alltweets))
    
    #transform the tweepy tweets into a 2D array that will populate the csv    
    outtweets = [[tweet.id_str.encode("utf-8"), tweet.created_at, tweet.text.encode("utf-8"),tweet.retweet_count,tweet.favorite_count,
		tweet.retweeted,tweet.source.encode("utf-8"),tweet.user.followers_count,tweet.user.friends_count,tweet.user.name.encode("utf-8"),tweet.user.created_at,tweet.user.screen_name.encode("utf-8"), tweet.lang] for tweet in alltweets]
    
    #write the csv    
    with open('tweets.csv', 'a') as f:
        writer = csv.writer(f)
        writer.writerows(outtweets)
    
    pass

#-----------------------------------------------------------------------

#-----------------------------------------------------------------------
# create twitter API object
#-----------------------------------------------------------------------
twitter = Twitter(
		auth = OAuth(access_key, access_secret, consumer_key, consumer_secret))

#-----------------------------------------------------------------------
# this is the user whose friends we will list
#-----------------------------------------------------------------------
username = "Mark Zuckerberg"

#-----------------------------------------------------------------------
# perform a basic search 
# twitter API docs: https://dev.twitter.com/rest/reference/get/friends/ids
#-----------------------------------------------------------------------
query = twitter.friends.ids(screen_name = username)

#-----------------------------------------------------------------------
# extract user information first

with open('tweets.csv', 'a') as f:
	writer = csv.writer(f)
	writer.writerow(["id","created_at","text","retweet_count","favorite_count","isRetweeted","source","followers_count","friends_count","name","user_created_at","screen_name","tweet_language"])
pass
get_all_tweets(username)
#-----------------------------------------------------------------------

#-----------------------------------------------------------------------
# tell the user how many friends we've found.
# note that the twitter API will NOT immediately give us any more 
# information about friends except their numeric IDs...
#-----------------------------------------------------------------------
print "found %d friends" % (len(query["ids"]))

#-----------------------------------------------------------------------
# now we loop through them to pull out more info, in blocks of 100.
#-----------------------------------------------------------------------
for n in range(0, len(query["ids"]), 100):
	ids = query["ids"][n:n+100]

	#-----------------------------------------------------------------------
	# create a subquery, looking up information about these users
	# twitter API docs: https://dev.twitter.com/rest/reference/get/users/lookup
	#-----------------------------------------------------------------------
	subquery = twitter.users.lookup(user_id = ids)

	for user in subquery:
		#-----------------------------------------------------------------------
		# now print out user info, starring any users that are Verified.
		#-----------------------------------------------------------------------
		print " [%s] %s - %s" % ("*" if user["verified"] else " ", user["screen_name"], user["location"])
		get_all_tweets(user["screen_name"])
