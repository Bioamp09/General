import json
import requests
apiKey = 'api_key=56e4a12d-bbdd-4572-9722-368d93494a51'
getNameRequest = "https://na.api.pvp.net/api/lol/na/v1.4/summoner/by-name/"
getRankedStats = "https://na.api.pvp.net/api/lol/na/v1.3/stats/by-summoner/"
rankedStats = "/ranked?season=SEASON2015&"
championParse = "https://global.api.pvp.net/api/lol/static-data/na/v1.2/champion/"
champParseTwo = "?" + apiKey


#summoner = requests.get("https://na.api.pvp.net/api/lol/na/v1.4/summoner/by-name/Bioamp09?api_key=56e4a12d-bbdd-4572-9722-368d93494a51");
#r.json
#print summoner.content

summonerRequest = raw_input('What summoner would you like to find? ')
print summonerRequest
fullRequest = getNameRequest + summonerRequest + '?' + apiKey
print fullRequest
newRequest = requests.get(fullRequest)
print newRequest.content

jsonInfo = open('info.json','w+')
jsonInfo.write(newRequest.text)
jsonInfo.close();

with  open('info.json', 'rw+') as jsonRead:
	jsonLoad = json.load(jsonRead)
	with open('output.json', 'rw+') as output:
		json.dump(jsonLoad, output, sort_keys = True, indent = 4)
		output.close();
	jsonRead.close();

#summonerRequest = raw_input('What summoner would you like to find? ')

#print summonerRequest
#fullRequest = getNameRequest + summonerRequest + '?' + apiKey
#print fullRequest
#newRequest = requests.get(fullRequest)
#print newRequest.content
#print ('Now Looking Up Ranked Stats...\n\n\n')
try:
	with open('output.json', 'r') as sumId:
		loader = json.load(sumId)
		summonerId = loader[summonerRequest.lower()]['id']
		print summonerId
		sumId.close()
		rankedLookup = getRankedStats + str(summonerId) + rankedStats + apiKey
		print rankedLookup
		rankedRequest = requests.get(rankedLookup)
		#print rankedRequest.content
except ValueError:
	print 'Decoding JSON has failed'
	
with open('ranked.json', 'w+') as writeRanked:
	writeRanked.write(rankedRequest.content)
	writeRanked.close()	

with open('ranked.json', 'rw+') as parseRanked:
	parse = json.load(parseRanked)
	with open('parsedRanked.json', 'rw+') as parsed:
		json.dump(parse, parsed, sort_keys = True, indent = 4)
		parsed.close()
	parseRanked.close()

rankedRequest = raw_input('What champion would you like stats for? ')
rankedRequest = rankedRequest.lower()

with open('parsedRanked.json', 'rw+') as champ:
	champObj = json.load(champ)
	for value in champObj['champions']:
		champRequest = requests.get(championParse + str(value['id']) + champParseTwo)
		print champRequest.content
		#champLoad = json.load(champRequest.content)
		#champName = champRequest['key'].lower()
		#if (rankedRequest == champName):
		#	identifier = str(value['id'])
		#	break
	#print identifier
		

