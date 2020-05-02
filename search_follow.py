import tweepy
import time
import random


# API_KEY =
# API_SECRET =
# ACCESS_TOKEN =
# ACCESS_SECRET =

file_name = 'last_id.txt'

class Main:
    auth = tweepy.OAuthHandler(API_KEY, API_SECRET)
    auth.set_access_token(ACCESS_TOKEN, ACCESS_SECRET)
    api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)
    user = api.me()

    # Auto search and follow
    query_list = ['buckeye', 'ohio state', 'tosu', '#gobucks', 'ohio state university']
    query = random.choice(query_list)
    max_tweets = 15
    count = 0
    iteration = 1
    while count <= max_tweets:
        for tweet in tweepy.Cursor(api.search, q=query).items(max_tweets*iteration):
            if not tweet.user.following:
                tweet.user.follow()
                count = count + 1
                iteration = iteration + 1
                time.sleep(10)

            if count >= max_tweets:
                break


if __name__ == '__main__':
    Main()
