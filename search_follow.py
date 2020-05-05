import tweepy
import time
import random
import datetime
from pytz import timezone

# API_KEY =
# API_SECRET =
# ACCESS_TOKEN =
# ACCESS_SECRET =

tz = timezone('US/Eastern')


def get_time():
    return str(datetime.datetime.strptime(str(datetime.datetime.now(tz).replace(microsecond=0, tzinfo=None)), '%Y-%m-%d %H:%M:%S').strftime('%I:%M %p'))


class Main:
    auth = tweepy.OAuthHandler(API_KEY, API_SECRET)
    auth.set_access_token(ACCESS_TOKEN, ACCESS_SECRET)
    api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)
    user = api.me()

    # Auto search and follow
    query_list = ['buckeye', 'ohio state', 'tosu', '#gobucks', 'ohio state university', 'go bucks', 'go buckeye']
    time_str = get_time()
    dm_message = 'Go Bucks! Time: ' + time_str
    query = random.choice(query_list)
    max_tweets = 1
    count = 0
    iteration = 1

    while count <= max_tweets:
        try:
            for tweet in tweepy.Cursor(api.search, q=query).items(max_tweets * iteration):
                # Follower user
                if not tweet.user.following:
                    tweet.user.follow()
                    count = count + 1
                    time.sleep(10)

                # Like first post
                try:
                    top_tweets = api.user_timeline(screen_name=tweet.user.screen_name,
                                                   count=1,
                                                   include_rts=False,
                                                   tweet_mode='extended'
                                                   )
                    print(top_tweets[0].user)
                    print(top_tweets[0].user.screen_name)
                    for t in top_tweets:
                        if not t.favorited:
                            t.favorite()
                            print('Top tweets favorited.')
                            time.sleep(10)

                except tweepy.TweepError as e:
                    print(e.reason)
                    time.sleep(10)

                # Send DM
                try:
                    api.send_direct_message(tweet.user.id, dm_message)
                    print('DM sent.')
                    time.sleep(10)
                except tweepy.TweepError as e:
                    print(e.reason)

        except tweepy.TweepError as e:
            print(e.reason)
            time.sleep(10)
            break

        iteration = iteration + 1
        if count >= max_tweets:
            break


if __name__ == '__main__':
    Main()
