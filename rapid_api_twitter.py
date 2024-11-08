import http.client
import json
import time
from GPT_api import sendTweetsToGPT

conn = http.client.HTTPSConnection("twitter241.p.rapidapi.com")

headers = {
    'x-rapidapi-key': "7c42dd07e2msh5006f8bd113275cp1cbf38jsn2c1910960576",
    'x-rapidapi-host': "twitter241.p.rapidapi.com"
}


def extractPinnedTweet(json_data):
    output = {}
    if json_data['result']['timeline']['instructions'][1]["type"] == "TimelinePinEntry":
        tweet_results = json_data['result']['timeline']['instructions'][1]['entry']['content']['itemContent']['tweet_results']['result']
        pinned_tweet = tweet_results['legacy']['full_text']
        if 'quoted_status_result' in tweet_results.keys():
            quoted_tweet = tweet_results['quoted_status_result']['result']['legacy']['full_text']
            output["pinned_tweet"] = pinned_tweet
            output["about"] = quoted_tweet
        else:
            output["pinned_tweet"] = pinned_tweet
    else:
        output["pinned_tweet"] = "This user has not pinned any tweet."
    return output

def extractTweets(json_data):
    tweets = []
    json_data_results = json_data['result']['timeline']['instructions']
    timeline_entries = json_data_results[len(json_data_results)-1]['entries']
    for t in timeline_entries:
        try:
            if 'itemContent' in t['content'].keys() and t['content']['itemContent']['itemType'] == "TimelineTweet":
                if 'quoted_status_result' in t['content']['itemContent']['tweet_results']['result'].keys():
                    tweets.append({"tweet": t['content']['itemContent']['tweet_results']['result']['legacy']['full_text'], 
                                "about": t['content']['itemContent']['tweet_results']['result']['quoted_status_result']['result']['legacy']['full_text']})
                else:
                    tweets.append({"tweet": t['content']['itemContent']['tweet_results']['result']['legacy']['full_text']})
        except KeyError as e:
            print(f"KeyError: Missing key {e} in tweet data. Skipping this entry.")
        except Exception as e:
            print(f"Unexpected error occurred: {e}. Skipping this entry.")
    return tweets


def getUserID(username):
    url = f"/user?username={username}"
    conn.request("GET", url, headers=headers)
    res = conn.getresponse()
    data = res.read()
    json_data = json.loads(data.decode("utf-8"))
    user_id = json_data['result']['data']['user']['result']['rest_id']
    time.sleep(1.001)                                   # API allows only 1 call per 1 second
    return user_id

def getTweets(username, num_tweets):
    count = 20
    total_tweets = num_tweets
    cursor_bottom = None
    pinned_tweet = {}
    all_tweets = []
    output = {}
    # user_id = '44196397'
    user_id = getUserID(username)

    for i in range(total_tweets // count):
        url = f"/user-tweets?user={user_id}&count={count}"
        
        if cursor_bottom:
            url += f"&cursor={cursor_bottom}"

        conn.request("GET", url, headers=headers)

        res = conn.getresponse()
        data = res.read()
        json_data = json.loads(data.decode("utf-8"))
        
        if json_data['result']['timeline']['instructions'][1]["type"] == "TimelinePinEntry":
            pinned_tweet = extractPinnedTweet(json_data)
            output["pinned_tweet"] = pinned_tweet

        tweets = extractTweets(json_data)
        all_tweets.extend(tweets)

        cursor_info = json_data.get("cursor", {})                 # Move cursor to the next set of tweets to fetch
        cursor_bottom = cursor_info.get("bottom")
        if not cursor_bottom:
            break 

        time.sleep(1.001)                                   # API allows only 1 call per 1 second
    
    output["tweets"] = all_tweets
    return output

print("")
target = input("Please enter the target's username in Twitter: ")
print("")

tweets_of_target = getTweets(target, 20)
# print(tweets_of_target)
with open("fetched_results.txt", "w", encoding="utf-8") as file:
    file.write(str(tweets_of_target))
    file.close()

output = sendTweetsToGPT(tweets_of_target)
print(output)
print("")

