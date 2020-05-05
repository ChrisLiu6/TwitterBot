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
    return str(datetime.datetime.strptime(str(datetime.datetime.now(tz).replace(microsecond=0, tzinfo=None)),
                                          '%Y-%m-%d %H:%M:%S').strftime('%I:%M %p'))


class Main:
    auth = tweepy.OAuthHandler(API_KEY, API_SECRET)
    auth.set_access_token(ACCESS_TOKEN, ACCESS_SECRET)
    api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)
    user = api.me()

    # Auto search and follow
    dm_message = 'Stay well and Go Bucks!'
    user_names = ['ohiostate', 'OhioStateNews', 'studentlifeOSU', 'ohiostatefb']
    user_name = random.choice(user_names)
    object = api.get_user(screen_name=user_name)
    count = 0
    max_users = 15
    iteration = 1

    while count <= max_users:
        for follower in tweepy.Cursor(api.followers, screen_name=user_name).items(20 * iteration):
            # Follower user followers
            if not follower.following:
                try:
                    # Follow if not followed
                    follower.follow()
                    count = count + 1
                    # print('User Name: ' + str(follower.screen_name) + ' Followed')

                    # Like first post
                    try:
                        top_tweets = api.user_timeline(screen_name=follower.screen_name,
                                                       count=3,
                                                       include_rts=False,
                                                       tweet_mode='extended'
                                                       )
                        for t in top_tweets:
                            if not t.favorited:
                                t.favorite()
                                # print('Top tweets favorited.')
                                time.sleep(10)

                    except tweepy.TweepError as e:
                        print(e.reason)
                        time.sleep(10)

                    """
                    # Send DM
                    try:
                        api.send_direct_message(follower.id, dm_message)
                        print('DM sent.')
                        time.sleep(10)
                    except tweepy.TweepError as e:
                        print(e.reason)
                    """

                    if count >= max_users:
                        break

                except tweepy.TweepError as e:
                    print(e.reason)

        iteration = iteration + 1

        if count >= max_users or iteration >= 10:
            break


if __name__ == '__main__':
    Main()
