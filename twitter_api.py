import requests

# username = "TheNBACentel"
url_for_userID = "https://api.twitter.com/2/users/by/username/"
url_for_tweets = "https://api.x.com/2/users/1547232242073849856/tweets"

token = "AAAAAAAAAAAAAAAAAAAAAG5MwwEAAAAAmrynSSJrQnP%2BQTIeKcs2N5Ku68Q%3Dfz4r9xH2rCp0R8VVF0aY5DJqLqYy0hT2CMYfSb57eaKhuJIkQP"

def getUserID(username: str):
    headers = {"Authorization" : f"Bearer {token}"}
    response = requests.get(url_for_userID + username, headers = headers)
    return response.json()

def getUserTweets(username: str):
    userID = getUserID(username)['data']['id']
    headers = {"Authorization" : f"Bearer {token}"}
    response = requests.get(f"https://api.x.com/2/users/{userID}/tweets", headers = headers)
    output = response.json()
    print(type(output))
    print(output)

getUserTweets("elonmusk")