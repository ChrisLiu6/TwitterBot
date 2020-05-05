import tweepy
import time
import datetime
from pytz import timezone

# API_KEY =
# API_SECRET =
# ACCESS_TOKEN =
# ACCESS_SECRET =

file_name = 'last_id.txt'
message_file = 'message_file.txt'
follower_id_file = 'follower_id.txt'

tz = timezone('US/Eastern')

follower_dict = {}


def get_time():
    return str(datetime.datetime.strptime(str(datetime.datetime.now(tz).replace(microsecond=0, tzinfo=None)), '%Y-%m-%d %H:%M:%S').strftime('%Y-%m-%d %I:%M:%S %p'))


def read_last_id():
    file = open(file_name, 'r')
    last_id = int(file.read().strip())
    file.close()
    return last_id


def write_last_id(last_id):
    file = open(file_name, 'w')
    file.write(str(last_id))
    file.close()


def read_message_file():
    file = open(message_file, 'r')
    message = str(file.read())
    file.close()
    return message


def write_message_file(message):
    open(message_file, 'w').close()
    file = open(message_file, 'w')
    file.write(message)
    file.close()


def read_follower_id():
    global follower_dict

    file = open(follower_id_file, 'r')
    list = str(file.read()).split('\n')
    file.close()

    # Convert string to int
    for i in range(len(list)):
        list[i] = int(list[i])

    # Convert to dictionary
    for i in list:
        follower_dict.update({i:''})


def write_follower_id(follower_id):
    global follower_dict

    file = open(follower_id_file, 'a')
    file.write('\n' + str(follower_id))
    file.close()

    # Update follower id dictionary
    follower_dict.update({follower_id:''})

"""
def follow_followers(api):
    global follwer_dict
    for follower in tweepy.Cursor(api.followers).items():
        # Follow if not followed
        try:
            if not follower.following:
                follower.follow()
                time.sleep(10)
        except tweepy.TweepError as e:
            print(e.reason)
            break

        '''
        if follower.id not in follower_dict:

            # Open file to write message
            message = '@' + str(follower.screen_name) + ' Welcome, may the clock tower watch over you. \nTime: ' + str(datetime.datetime.now(tz).replace(microsecond=0, tzinfo=None))
            write_message_file(message)

            # Read and send content
            api.update_status(read_message_file())


            # Add follower to the dict
            write_follower_id(follower.id)
            time.sleep(10)
        '''
"""


def favorite_tweet(tweet, api):
    try:
        if not tweet.favorited:
            # Mark it as Liked, since we have not done it yet
            tweet.favorite()
    except tweepy.TweepError as e:
        print(e.reason)


class Main:
    auth = tweepy.OAuthHandler(API_KEY, API_SECRET)
    auth.set_access_token(ACCESS_TOKEN, ACCESS_SECRET)
    api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)
    user = api.me()

    read_follower_id()

    while True:
        for i in range(180):
            # Read Last Mention ID
            last_id = read_last_id()

            """
            # Auto follow
            follow_followers(api)
            """

            # Mentions
            mentions = api.mentions_timeline(last_id, tweet_mode='extended')

            if not mentions:
                pass
            else:
                for mention in reversed(mentions):
                    if str(mention.user.screen_name) != 'Real_ClockTower':
                        try:
                            # Favorite mention
                            favorite_tweet(mention, api)
                            time.sleep(5)

                            # Set response message
                            mention_text = str(mention.full_text).split(' ')
                            OHIO_list = {'oh', 'oh!', 'oh-'}
                            for index, word in enumerate(mention_text):
                                time = get_time()
                                if word.lower() in OHIO_list:
                                    resp = ' IO!\nTime: ' + time
                                else:
                                    resp = ' Go bucks!\n Time: ' + time

                            # Reply message
                            message = '@' + str(mention.user.screen_name) + resp
                            write_message_file(message)
                            api.update_status(read_message_file())
                            write_last_id(mention.id)

                            time.sleep(20)
                            break
                        except tweepy.TweepError as e:
                            print(e.reason)
                            break
            time.sleep(20)


if __name__ == '__main__':
    Main()
