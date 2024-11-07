import http.client
import json

conn = http.client.HTTPSConnection("twitter241.p.rapidapi.com")

headers = {
    'x-rapidapi-key': "7c42dd07e2msh5006f8bd113275cp1cbf38jsn2c1910960576",
    'x-rapidapi-host': "twitter241.p.rapidapi.com"
}

conn.request("GET", "/user-tweets?user=44196397&count=3", headers=headers)

res = conn.getresponse()
data = res.read()
json_data = json.loads(data.decode("utf-8"))
# print(type(res))
# print(type(data))
print(json_data['result']['timeline']['instructions'][1]['entry']['content']['itemContent']['tweet_results']['result']['legacy']['full_text'])
print(json_data['result']['timeline']['instructions'][1]['entry']['content']['itemContent']['tweet_results']['result']['quoted_status_result']['result']['legacy']['full_text'])

timeline_entries = json_data['result']['timeline']['instructions'][2]['entries']

tweets = []
for t in timeline_entries:
    if 'itemContent' in t['content'].keys() and t['content']['itemContent']['itemType'] == "TimelineTweet":
        if 'quoted_status_result' in t['content']['itemContent']['tweet_results']['result'].keys():
            tweets.append({"tweet": t['content']['itemContent']['tweet_results']['result']['legacy']['full_text'], 
                        "about": t['content']['itemContent']['tweet_results']['result']['quoted_status_result']['result']['legacy']['full_text']})
        else:
            tweets.append({"tweet": t['content']['itemContent']['tweet_results']['result']['legacy']['full_text']})
print(tweets)
