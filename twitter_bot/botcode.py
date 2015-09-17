from twython import Twython
import json

#opens the access.json file which has all our keys that we need and creates a Twython object based off of them
def auth():
	with open("access.json", 'r') as f:
		db = json.load(f)
	#	print (db["API_Key"], db["API_Secret"], db["Access_Token"], db["Access_Token_Secret"])
	return Twython(db["API_Key"], db["API_Secret"], db["Access_Token"], db["Access_Token_Secret"])

def load():
	#ensures that the file queue.json is closed after we store it in our queue
	with open("queue.json", 'r') as f:
		queue = json.load(f)
	#ensures that the file info.json is closed after we store it in our queue
	with open("info.json", 'r') as fi:
		info = json.load(fi)
	#returns the queue and info we just stored
	return queue, info

#saves the data and dumps it into our files
def dump(queue, info):
	with open("queue.json", 'w') as f:
		json.dump(queue, f)
	with open("info.json", 'w') as fi:
		json.dump(info, fi)

#our response function to respond to tweets
def respond(twitter, top_tweet):
	#extract the tweet authors handle and add it into our own tweet
	name = top_tweet["user"]["screen_name"]
	twitter.update_status(status = "@%s @FosterThePrson \nFoster! Why is the wifi bad?" %(name), in_reply_to_status_id = top_tweet["id"])

def main():
	#grabs the necessary information from our json file and stores it as a Twython object known as twitter for us
	twitter = auth()
	
	#adds tweets to respond to into our queue
	queue, info = load()

	triggers = ["Mizzou Wireless", "TigerWifi", "Tiger Wifi"]	
	#returns a dictionary with 2 elements, 1 with metadata for what we are currently querying as the value and one with the list of tweets.
	tweets = twitter.search(q=triggers, result_type = "recent", since_id = info["sinceid"], count = '100')
	
	#stores the id of the most recent tweet that our search found and stores it into the dictionary, this way we don't keep adding the same tweet over and over again.
	#This is stored in the info.json to be used with our query
	info["sinceid"] = tweets["search_metadata"]["max_id"]
	
	#the words that trigger our bot to respond'
	#triggers = ("Mizzou Wirless", "TigerWifi", "Tiger Wifi");

	#filters out tweets that have been retweeted
	to_add = [tweet for tweet in tweets["statuses"] if not tweet["retweeted"] and not tweet.has_key("retweeted_status")]
	to_add = [tweet for tweet in to_add if tweet["text"].startswith(triggers) or tweet["text"].split(" ",1)[1].startswith(triggers)]
	
	#adds tweets to the queue that have yet to be responded to.
	queue = queue + to_add
	#this is our max number of tweets we will hold in the queue, we don't want to overfill our queue and run out of disk space on our machines
	mx = max(len(to_add), 20)
	if len(queue) > mx:
		queue = queue[-mx:]
	#auto response if our queue has things in it but less than our max.
	if len(queue) > 0:
		respond(twitter, queue.pop())
	
	dump(queue, info)
	print ("Bot successfully ran!")
#run on cron every minute
if __name__ == "__main__":
	main()
