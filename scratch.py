import http.client
import json
import time
# Define the connection parameters
conn = http.client.HTTPSConnection("twitter241.p.rapidapi.com")
headers = {
    'x-rapidapi-key': "7c42dd07e2msh5006f8bd113275cp1cbf38jsn2c1910960576",
    'x-rapidapi-host': "twitter241.p.rapidapi.com"
}

# Initialize variables for pagination and data collection
user_id = "44196397"  # Example user ID
count = 20  # Number of tweets per request
total_tweets = 1000  # Total number of tweets you want to fetch
all_tweets = []
cursor_bottom = None  # Starting cursor (None or empty for the first request)

# Loop to fetch 100 tweets in 5 requests
for _ in range(total_tweets // count):
    # Construct the URL with the cursor if it's not None
    url = f"/user-tweets?user={user_id}&count={count}"
    if cursor_bottom:
        url += f"&cursor={cursor_bottom}"
    
    # Make the HTTP GET request
    conn.request("GET", url, headers=headers)
    res = conn.getresponse()
    data = res.read()
    time.sleep(1.001)
    # Decode and parse the JSON response
    response = json.loads(data.decode("utf-8"))
    tweets = []
    for i in range(count):
        # Extract tweets and append them to the all_tweets list
        a = response['result']['timeline']['instructions']
        data = a[len(a) - 1]['entries'][i]['content']

        if 'itemContent' in data:
            tweet = data['itemContent']['tweet_results']['result']['legacy']['full_text']
        else:
            print(data)
        
        tweets.append(tweet)
    all_tweets.extend(tweets)

    # Get the next cursor for pagination using the `bottom` cursor
    cursor_info = response.get("cursor", {})
    cursor_bottom = cursor_info.get("bottom")
    if not cursor_bottom:
        break  # If there's no `bottom` cursor, stop fetching
    
    print(f"Fetched {len(tweets)} tweets, moving to next page with cursor: {cursor_bottom}")

# Print the collected tweets (pretty-printed for clarity)
print(json.dumps(all_tweets, indent=4))

# Total number of tweets fetched
print(f"Total tweets fetched: {len(all_tweets)}")
