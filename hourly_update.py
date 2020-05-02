import tweepy
import datetime
from pytz import timezone

# API_KEY =
# API_SECRET =
# ACCESS_TOKEN =
# ACCESS_SECRET =

time_file = 'time_file.txt'
tz = timezone('US/Eastern')


def get_time():
    return str(datetime.datetime.strptime(str(datetime.datetime.now(tz).replace(minute=0, second=0, microsecond=0, tzinfo=None)), '%Y-%m-%d %H:%M:%S').strftime('%I:%M %p'))


def read_time_file():
    file = open(time_file, 'r')
    message = str(file.read())
    file.close()
    return message


def write_time_file(message):
    open(time_file, 'w').close()
    file = open(time_file, 'w')
    file.write(message)
    file.close()


class Main:
    auth = tweepy.OAuthHandler(API_KEY, API_SECRET)
    auth.set_access_token(ACCESS_TOKEN, ACCESS_SECRET)
    api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)
    user = api.me()

    time = get_time()

    message = "BONG!\n\nIt's " + time + ' and Michigan still sucks. Go Bucks!'
    write_time_file(message)
    api.update_status(read_time_file())


if __name__ == '__main__':
    Main()
