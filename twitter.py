from twython import TwythonStreamer
import json
import argparse


# instead of entering the keys/secrets as strings in the following fields,
# they will be read from the hidden files:
with open('.consumer_key', 'r') as _ck_file:
    _consumer_key: str = _ck_file.readline().strip()
with open('.consumer_secret', 'r') as _cs_file:
    _consumer_secret: str = _cs_file.readline().strip()
with open('.access_token', 'r') as _at_file:
    _access_token: str = _at_file.readline().strip()
with open('.access_secret', 'r') as _as_file:
    _access_secret: str = _as_file.readline().strip()

# credentials dictionary
credentials = {
    'CONSUMER_KEY': _consumer_key,
    'CONSUMER_SECRET': _consumer_secret,
    'ACCESS_TOKEN': _access_token,
    'ACCESS_SECRET': _access_secret,
}


# we filter out unwanted data
def process_tweet(tweet) -> dict:
    d = {
        'hashtags': [hashtag['text'] for hashtag in
                     tweet['entities']['hashtags']],
        'user': tweet['user'],
        'created_at': tweet['created_at'],
        'geo': tweet['geo'],
        'reply_count': tweet['reply_count'],
        'retweet_count': tweet['retweet_count'],
        'favorite_count': tweet['favorite_count'],
        'id': tweet['id_str'],
        'in_reply_to_status_id': tweet['in_reply_to_status_id_str'],
        'in_reply_to_user_id_str': tweet['in_reply_to_user_id_str'],
    }
    return d


# we create a class that inherits TwythonStreamer
class MyStreamer(TwythonStreamer):
    count = 0

    # received data
    def on_success(self, data):

        # Only collect tweets in English
        if data['lang'] == 'en':
            tweet_data = process_tweet(data)
            self.save_to_csv(data)
            self.count += 1
            if self.count % 100 == 0:
                print("tweet received: " + str(self.count))

    # problem with the API
    def on_error(self, status_code, data, headers=None):
        print(status_code, data)
        self.disconnect()

    # save each tweet to csv file
    @staticmethod
    def save_to_csv(tweet):
        with open('corona_tweet.json', 'a') as fp:
            json.dump(tweet, fp)
            fp.write("\n")


# ###################################################################
# MAIN EXECUTION
# ###################################################################

# we add an argument parser to ex
parser = argparse.ArgumentParser(
    description='Store some Twitter data: both locally or in a '
                'MongoDB database if --mongo is flagged')
parser.add_argument(
    '-mdb', '--mongodb', action='store_true',
    help='If activated, the tweet data is stored in a MongoDB '
         'database instead of a local .json')
# now the 'mongodb' state is added as local variable in the
# args namespace (by default, set to False)
args = parser.parse_args()
# the variable can be accessed as vars(args)['mongodb']

# Instantiate from our streaming class
stream = MyStreamer(credentials['CONSUMER_KEY'],
                    credentials['CONSUMER_SECRET'],
                    credentials['ACCESS_TOKEN'], credentials['ACCESS_SECRET'])
# start the stream
stream.statuses.filter(track='corona')

if vars(args)['mongodb']:
    raise Exception("Storing the tweet data into a MongoDB "
                    "database is still not implemented")
else:
    print("Initializing the MyStreamer")
