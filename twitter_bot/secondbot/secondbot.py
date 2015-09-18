from twython import Twython, TwythonError
import time
import json

APP_KEY = 'f4GyExdy6V2zKf0kb3ZFqBL07'
APP_SECRET = 'xrG7z7Fs4hcE6EqCbxfEHMcDmxDurYxogw9l1xJpM4ci70ZLKS'
OATH_TOKEN = '3595801464-WX9eZo9xerpvxnfhuS0W6DsmOYMQoXAALqASQ98'
OATH_TOKEN_SECRET = 'jjx3PTORO9k7ZmKXNZVRU0pIAevL3OiSAk7q8wXTu9362'

twitter = Twython(APP_KEY, APP_SECRET, OATH_TOKEN, OATH_TOKEN_SECRET)

try:
	with open('liners.txt', 'r+') as tweetfile:
		buff = tweetfile.readlines()
	with open('searchedItems.json', 'w') as f:
		result = twitter.search(q='11 ounce steak in 3 minutes 30 secs', result_type = 'recent', count =1)
		json.dump(result, f, sort_keys = True, indent = 4)
	
#	print(twitter.search(q='Bioamp09', result_type = 'recent', count = 1))
	
	with open('searchedItems.json', 'r+') as f1:
		info = json.load(f1)
		print ("\n\n\n")
		print (info["statuses"][0]["id"])
		idnum = info["statuses"][0]["id"]
		status = "MUWifiAlertBot: Testing Protocols..."
		twitter.update_status(status="Testing inherent protocols...", in_reply_to_status_id = info["statuses"][0]["id"])
	
	for line in buff[:]:
		line = line.strip(r'\n') #Strips any empty line.
		if len(line)<=140 and len(line)>0:
			print ("Tweeting...")
			twitter.update_status(status=line)
			with open ('liners.txt', 'w') as tweetfile:
				buff.remove(line) #Removes the tweeted line.
				tweetfile.writelines(buff)
		#time.sleep(900)
		else:
			with open ('liners.txt', 'w') as tweetfile:
				buff.remove(line) #Removes the line that has more than 140 characters.
				tweetfile.writelines(buff)
			print ("Skipped line - Char length violation")
			continue
	print ("No more lines to tweet...") #When you see this... Well :) Go find some new tweets...

except TwythonError as e:
		print (e)


#user_timeline = twitter.getUserTimeline(screen_name="MUWifiAlertBot")

#for tweet in user_timeline:
#try:
#	print(twitter.search(q='Mizzou Wireless', count = 10)

#searchedItems = twitter.search(q='Mizzou Wireless', result_type = 'recent', count = 100)

#for tweet in searchedItems['statuses']:
#	print(tweet['text'])
#with open("searchedItems.json", 'w') as jsonFile:
#json.dump(searchedItems, jsonFile)
